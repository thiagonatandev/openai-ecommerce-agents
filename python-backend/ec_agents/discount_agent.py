from typing import Optional
from agents import Agent, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.apply_discount_code import apply_discount_code
from tools.list_valid_promotions import list_valid_promotions
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore


def discount_agent_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Discount Agent. Follow this routine:\n"
        f"1. The customer may ask about discount codes or current promotions for their order.\n"
        f"2. If the order number is available, use the `list_valid_promotions` tool to show promotions valid for that order.\n"
        f"3. If the customer provides a discount code to apply, use the `apply_discount_code` tool with the order number and code.\n"
        f"4. If the discount code is invalid or already used, inform the customer accordingly.\n"
        f"5. If the customer does not provide an order number, ask them to provide it.\n"
        "6. If the question is unrelated to discounts or promotions, transfer back to the triage agent.\n"
        "7. If the customer asks anything else, transfer back to the triage agent.\n"
    )



discount_agent = Agent[ECommerceAgentContext](
    name="Discount Agent",
    model="gpt-4.1",
    handoff_description="Provides information about coupons and promotions.",
    instructions=discount_agent_instructions,
    tools=[apply_discount_code, list_valid_promotions],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)
