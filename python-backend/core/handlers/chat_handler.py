from typing import List, Dict, Any
from uuid import uuid4
import time
import json
import uuid

from agents import (
    Runner,
    ItemHelpers,
    MessageOutputItem,
    HandoffOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
    InputGuardrailTripwireTriggered,
    Handoff,
)

from models.agent_event import AgentEvent
from models.chat_request import ChatRequest
from models.chat_response import ChatResponse
from models.guardrail_check import GuardrailCheck
from models.message_response import MessageResponse
from context.ecommerce_context import ECommerceAgentContext, create_initial_context
from core.registry.agent_registry import AGENTS, DEFAULT_AGENT
from core.helpers.build_agents_list import build_agents_list
from core.helpers.get_guardrail_name import get_guardrail_name
from core.store import conversation_store

def get_agent(name: str):
    return AGENTS.get(name, DEFAULT_AGENT)

def generate_conversation_id():
    return str(uuid.uuid4())

async def handle_chat_request(req: ChatRequest) -> ChatResponse:
    if not req.conversation_id:
        req.conversation_id = generate_conversation_id()

    conversation = conversation_store.get(req.conversation_id)

    if conversation is None:
        ctx = create_initial_context()
        state = {
            "input_items": [],
            "context": ctx,
            "current_agent": DEFAULT_AGENT.name,
            "messages": [],
            "events": [],
            "agents": build_agents_list(),
            "guardrails": [],
        }
        conversation_store.save(req.conversation_id, state)
        conversation = state
    else:
        if isinstance(conversation.get("context"), dict):
            conversation["context"] = ECommerceAgentContext.model_validate(conversation["context"])

    state = conversation

    if not req.message.strip():
        return ChatResponse(
            conversation_id=req.conversation_id,
            current_agent=state["current_agent"],
            context=state.get("context", {}).model_dump() if hasattr(state["context"], "model_dump") else state["context"],
            messages=state.get("messages", []),
            agents=state.get("agents", []),
            events=state.get("events", []),
            guardrails=state.get("guardrails", []),
        )

    current_agent = get_agent(state["current_agent"])
    state["input_items"].append({"content": req.message, "role": "user"})

    state.setdefault("messages", []).append({
        "content": req.message,
        "role": "user",
        "agent": "user"
    })

    old_context = state["context"].model_dump().copy()
    guardrail_checks = []

    try:
        result = await Runner.run(current_agent, state["input_items"], context=state["context"])
    except InputGuardrailTripwireTriggered as e:
        failed = e.guardrail_result.guardrail
        gr_output = e.guardrail_result.output.output_info
        gr_reasoning = getattr(gr_output, "reasoning", "")
        gr_timestamp = time.time() * 1000

        for g in current_agent.input_guardrails:
            guardrail_checks.append(GuardrailCheck(
                id=uuid4().hex,
                name=get_guardrail_name(g),
                input=req.message,
                reasoning=(gr_reasoning if g == failed else ""),
                passed=(g != failed),
                timestamp=gr_timestamp,
            ))

        refusal = "Sorry, I can only answer questions related to orders assistance."
        state["input_items"].append({"role": "assistant", "content": refusal})
        state["messages"].append({
            "content": refusal,
            "role": "assistant",
            "agent": current_agent.name ,
        })

        conversation_store.save(req.conversation_id, state)
        return ChatResponse(
            conversation_id=req.conversation_id,
            current_agent=current_agent.name,
            messages=[MessageResponse(content=refusal, agent=current_agent.name)],
            events=[],
            context=state["context"].model_dump(),
            agents=build_agents_list(),
            guardrails=guardrail_checks,
        )

    messages = []
    events = []

    for item in result.new_items:
        if isinstance(item, MessageOutputItem):
            text = ItemHelpers.text_message_output(item)
            messages.append(MessageResponse(content=text, agent=item.agent.name, role="assistant"))
            events.append(AgentEvent(id=uuid4().hex, type="message", agent=item.agent.name, content=text))
        elif isinstance(item, HandoffOutputItem):
            events.append(AgentEvent(
                id=uuid4().hex,
                type="handoff",
                agent=item.source_agent.name,
                content=f"{item.source_agent.name} -> {item.target_agent.name}",
                metadata={"source_agent": item.source_agent.name, "target_agent": item.target_agent.name},
            ))
            ho = next((h for h in getattr(item.source_agent, "handoffs", [])
                       if isinstance(h, Handoff) and getattr(h, "agent_name", None) == item.target_agent.name), None)
            if ho:
                fn = ho.on_invoke_handoff
                if "on_handoff" in fn.__code__.co_freevars:
                    cb = fn.__closure__[fn.__code__.co_freevars.index("on_handoff")].cell_contents
                    if cb:
                        cb_name = getattr(cb, "__name__", repr(cb))
                        events.append(AgentEvent(
                            id=uuid4().hex,
                            type="tool_call",
                            agent=item.target_agent.name,
                            content=cb_name,
                        ))
            current_agent = item.target_agent
        elif isinstance(item, ToolCallItem):
            tool_name = getattr(item.raw_item, "name", None)
            raw_args = getattr(item.raw_item, "arguments", None)
            tool_args = raw_args
            if isinstance(raw_args, str):
                try:
                    tool_args = json.loads(raw_args)
                except Exception:
                    pass
            events.append(AgentEvent(
                id=uuid4().hex,
                type="tool_call",
                agent=item.agent.name,
                content=tool_name or "",
                metadata={"tool_args": tool_args},
            ))
        elif isinstance(item, ToolCallOutputItem):
            events.append(AgentEvent(
                id=uuid4().hex,
                type="tool_output",
                agent=item.agent.name,
                content=str(item.output),
                metadata={"tool_result": item.output},
            ))

    new_context = state["context"].dict()
    changes = {k: new_context[k] for k in new_context if old_context.get(k) != new_context[k]}
    if changes:
        events.append(AgentEvent(
            id=uuid4().hex,
            type="context_update",
            agent=current_agent.name,
            content="",
            metadata={"changes": changes},
        ))

    state["input_items"] = result.to_input_list()
    state["current_agent"] = current_agent.name
    state["messages"].extend([{
        "content": m.content,
        "role": "user" if m.agent is None or m.agent == "user" else "assistant",
        "agent": m.agent,
    } for m in messages])
    
    state["events"].extend([e.model_dump() for e in events])
    state["agents"] = build_agents_list()
    final_guardrails = []
    for g in getattr(current_agent, "input_guardrails", []):
        name = get_guardrail_name(g)
        failed = next((gc for gc in guardrail_checks if gc.name == name), None)
        if failed:
            final_guardrails.append(failed)
        else:
            final_guardrails.append(GuardrailCheck(
                id=uuid4().hex,
                name=name,
                input=req.message,
                reasoning="",
                passed=True,
                timestamp=time.time() * 1000,
            ))

    state["guardrails"] = [g.model_dump() for g in final_guardrails]
    conversation_store.save(req.conversation_id, state)

    return ChatResponse(
        conversation_id=req.conversation_id,
        current_agent=current_agent.name,
        messages=messages,
        events=events,
        context=state["context"].dict(),
        agents=state["agents"],
        guardrails=final_guardrails,
    )
