import string
from agents import Agent, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.product_faq import get_product_faq
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore
import random as rnd

def product_faq_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    product_id = ctx.product_id or "[unknown]"

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Product FAQ Agent. Follow this routine:\n"
        f"1. The customer wants information about product ID: {product_id}.\n"
        "2. Use the `get_product_faq` tool to provide FAQs including size guide, composition, video, and reviews.\n"
        "If the customer asks something unrelated to product FAQs, transfer back to the triage agent."
        "If the customer asks anything else, transfer back to the triage agent."
    )


product_faq_agent = Agent[ECommerceAgentContext](
    name="Product FAQ Agent",
    model="gpt-4.1",
    handoff_description="Answers questions about products.",
    instructions=product_faq_instructions,
    tools=[get_product_faq],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

async def on_product_faq_handoff(
    context: RunContextWrapper[ECommerceAgentContext]
) -> None:
    """Ensure product_id is present for product FAQ agent."""
    if context.context.product_id is None:
        context.context.product_id = ''.join(rnd.choices(string.ascii_uppercase + string.digits, k=8))