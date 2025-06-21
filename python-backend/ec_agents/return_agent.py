import random as rnd
import string
from agents import Agent, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from tools.initiate_return import initiate_return
from tools.check_return_policy import check_return_policy
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX  # type: ignore


def return_agent_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    order_number = ctx.order_number or "[unknown]"
    product_id = ctx.product_id or "[unknown]"
    reason = ctx.return_reason or "[unknown]"

    return (
        f"{RECOMMENDED_PROMPT_PREFIX}\n"
        "You are a Return Agent. Follow this routine:\n"
        f"1. The order number is {order_number}, the product_id is {product_id} and the reason is {reason}, \n"
        " If any of them are unknown, ask the customer to inform such \n"
        f"2. The customer wants to return or exchange a product. Order number: {order_number}, Product ID: {product_id}.\n"
        "3. Use the `check_return_policy` tool to verify if the product can be returned or exchanged.\n"
        f"4. If allowed, ask the customer for the reason if missing.\n"
        f"5. Next, use the `initiate_return` tool with the {order_number}, the {product_id} and {reason} to start the return process.\n"
        "6. Provide the return label URL and status to the customer.\n"
        "If the question is unrelated, transfer back to the order triage agent."
        "If the customer asks anything else, transfer back to the order triage agent."
    )


return_agent = Agent[ECommerceAgentContext](
    name="Return Agent",
    model="gpt-4.1",
    handoff_description="Processes return or exchange requests.",
    instructions=return_agent_instructions,
    tools=[check_return_policy, initiate_return],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)
