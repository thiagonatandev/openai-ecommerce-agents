from typing import Optional
from agents import Agent, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.apply_discount_code import apply_discount_code
from tools.list_active_promotions import list_active_promotions
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore


def discount_agent_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    user_id = ctx.user_id
    code = ctx.discount_code or "[unknown]"

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Discount Agent. Follow this routine:\n"
        f"1. The customer may ask about discount codes or current promotions.\n"
        f"2. If a discount code is provided (code: {code}), use the `apply_discount_code` tool to validate if it has not yet been used.\n"
        f"3. To list promotions, use the `list_active_promotions` tool (user ID: {user_id}).\n"
        f"4. If the customer selects one of the promotions sent, use the `apply_discount_code' tool with the code of the promotion selected.\n"
        "If the question is unrelated to discounts or promotions, transfer back to the triage agent."
        "If the customer asks anything else, transfer back to the triage agent."
    )


discount_agent = Agent[ECommerceAgentContext](
    name="Discount Agent",
    model="gpt-4.1",
    handoff_description="Provides information about coupons and promotions.",
    instructions=discount_agent_instructions,
    tools=[apply_discount_code, list_active_promotions],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)
