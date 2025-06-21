from core.registry.agent_registry import AGENTS
from core.helpers.get_guardrail_name import get_guardrail_name

def build_agents_list():
    def make_agent_dict(agent):
        return {
            "name": agent.name,
            "description": getattr(agent, "handoff_description", ""),
            "handoffs": [getattr(h, "agent_name", getattr(h, "name", "")) for h in getattr(agent, "handoffs", [])],
            "tools": [getattr(t, "name", getattr(t, "__name__", "")) for t in getattr(agent, "tools", [])],
            "input_guardrails": [get_guardrail_name(g) for g in getattr(agent, "input_guardrails", [])],
        }
    return [make_agent_dict(agent) for agent in AGENTS.values()]