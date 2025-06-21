from agents import Agent, handoff
from ec_agents.order_status_agent import order_status_agent
from ec_agents.return_agent import return_agent
from ec_agents.product_faq_agent import product_faq_agent, on_product_faq_handoff
from ec_agents.discount_agent import discount_agent
from ec_agents.payment_agent import payment_agent
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from context.ecommerce_context import ECommerceAgentContext
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX # type: ignore

triage_agent = Agent[ECommerceAgentContext](
    name="Triage Agent",
    model="gpt-4.1",
    handoff_description="A order triage agent that can delegate a customer's request to the appropriate agent.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful order triaging agent. You can use your tools to delegate questions to other appropriate agents."
    ),
    handoffs=[
        order_status_agent,
        return_agent,
        handoff(agent=product_faq_agent, on_handoff=on_product_faq_handoff),
        discount_agent,
        payment_agent,
    ],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)