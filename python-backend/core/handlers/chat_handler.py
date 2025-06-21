from typing import List, Dict, Any
from uuid import uuid4
import time
import json

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
from context.ecommerce_context import create_initial_context
from core.registry.agent_registry import AGENTS, DEFAULT_AGENT
from core.helpers.build_agents_list import build_agents_list
from core.helpers.get_guardrail_name import get_guardrail_name
from core.store import conversation_store

def get_agent(name: str):
    return AGENTS.get(name, DEFAULT_AGENT)

async def handle_chat_request(req: ChatRequest) -> ChatResponse:
    is_new = not req.conversation_id or conversation_store.get(req.conversation_id) is None

    if is_new:
        conversation_id = uuid4().hex
        ctx = create_initial_context()
        current_agent_name = DEFAULT_AGENT.name
        state = {
            "input_items": [],
            "context": ctx,
            "current_agent": current_agent_name,
        }
        if req.message.strip() == "":
            conversation_store.save(conversation_id, state)
            return ChatResponse(
                conversation_id=conversation_id,
                current_agent=current_agent_name,
                messages=[],
                events=[],
                context=ctx.model_dump(),
                agents=build_agents_list(),
                guardrails=[],
            )
    else:
        conversation_id = req.conversation_id
        state = conversation_store.get(conversation_id)

    current_agent = get_agent(state["current_agent"])
    state["input_items"].append({"content": req.message, "role": "user"})
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
        refusal = "Sorry, I can only answer questions related to airline travel."
        state["input_items"].append({"role": "assistant", "content": refusal})
        return ChatResponse(
            conversation_id=conversation_id,
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
            messages.append(MessageResponse(content=text, agent=item.agent.name))
            events.append(AgentEvent(id=uuid4().hex, type="message", agent=item.agent.name, content=text))
        elif isinstance(item, HandoffOutputItem):
            events.append(AgentEvent(
                id=uuid4().hex,
                type="handoff",
                agent=item.source_agent.name,
                content=f"{item.source_agent.name} -> {item.target_agent.name}",
                metadata={"source_agent": item.source_agent.name, "target_agent": item.target_agent.name},
            ))
            ho = next(
                (h for h in getattr(item.source_agent, "handoffs", [])
                 if isinstance(h, Handoff) and getattr(h, "agent_name", None) == item.target_agent.name),
                None,
            )
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
            if tool_name == "display_seat_map":
                messages.append(MessageResponse(content="DISPLAY_SEAT_MAP", agent=item.agent.name))
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
    conversation_store.save(conversation_id, state)

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

    return ChatResponse(
        conversation_id=conversation_id,
        current_agent=current_agent.name,
        messages=messages,
        events=events,
        context=state["context"].dict(),
        agents=build_agents_list(),
        guardrails=final_guardrails,
    )
