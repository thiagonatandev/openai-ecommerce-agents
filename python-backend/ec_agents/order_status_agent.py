import random as rnd
import string
from agents import Agent, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.track_order import track_order
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore

def order_status_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    order_number = ctx.order_number or "[unknown]"
    customer_email = ctx.customer_email or "[unknown]"

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are an Order Status Agent. Follow these steps to assist the customer:\n"
        f"1. The customer's email is {customer_email} and the order number is {order_number}.\n"
        "If either is unknown, ask the customer for the missing information. If both are known, confirm with the customer.\n"
        "2. Use the `track_order` tool to retrieve the order's status.\n"
        "If the customer asks something unrelated to order status, transfer back to the order triage agent."
        "If the customer asks anything else, transfer back to the order triage agent."
    )

order_status_agent = Agent[ECommerceAgentContext](
    name="Order Status Agent",
    model="gpt-4.1",
    handoff_description="Consulta e informa o status de pedidos.",
    instructions=order_status_instructions,
    tools=[track_order],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)
