import random as rnd
import string
from agents import Agent, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.get_payment_status import get_payment_status
from tools.resend_payment_link import resend_payment_link
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore


def payment_agent_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    payment_id = ctx.payment_id or "[unknown]"
    order_number = ctx.order_number or "[unknown]"

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are the Payment Agent. Your role is to assist customers with payment-related issues only.\n\n"
        "Follow these instructions strictly:\n"
        f"1. The current `payment_id` is: {payment_id}. If it is `[unknown]`, ask the user to provide a valid payment ID.\n"
        "   Once you receive a valid payment ID from the user, call the `get_payment_status` tool to retrieve the payment status.\n\n"
        f"2. The current `order_number` is: {order_number}. If the user explicitly asks to resend the payment link and an order number is available, use the `resend_payment_link` tool.\n"
        "   If the order number is missing, ask the user to provide it before proceeding with the resend.\n\n"
        "3. If the user asks about anything unrelated to payment (e.g., product info, delivery time, returns, order tracking), DO NOT respond directly.\n"
        "  Instead, perform a handoff back to the Order Triage Agent.\n\n"
        "If the question is unrelated to payment issues, transfer back to the order triage agent."
        "If the customer asks anything else, transfer back to the order triage agent."
    )


payment_agent = Agent[ECommerceAgentContext](
    name="Payment Agent",
    model="gpt-4.1",
    handoff_description="Handles payment-related inquiries.",
    instructions=payment_agent_instructions,
    tools=[get_payment_status, resend_payment_link],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)

