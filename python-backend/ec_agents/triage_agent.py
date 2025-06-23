from agents import Agent, RunContextWrapper, handoff
from ec_agents.order_status_agent import order_status_agent
from ec_agents.return_agent import return_agent
from ec_agents.product_faq_agent import product_faq_agent, on_product_faq_handoff
from ec_agents.discount_agent import discount_agent
from ec_agents.payment_agent import payment_agent
from guardrails.relevance import relevance_guardrail
from guardrails.jailbreak import jailbreak_guardrail
from context.ecommerce_context import ECommerceAgentContext
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX # type: ignore
from tools.validate_user import validate_user

def triage_agent_instructions(
    run_context: RunContextWrapper[ECommerceAgentContext], agent: Agent[ECommerceAgentContext]
) -> str:
    ctx = run_context.context
    user_email = ctx.customer_email or "[unknown]"
    return (
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful order triaging agent. You can use your tools to delegate questions to other appropriate agents.\n"
        "You need to follow this routine: \n"
        f"1. The user email is {user_email}. If is unknown, first of all, ask the customer for the email \n"
        "2. Validate if the user_email is valid using the tool: `validate_user` passing the email\n"
        "3. If the email is invalid, return to the first step, and ask the email again\n"
        "4. If the email is valid, you can delegate the questions to other appropriate agents."
    )
    
triage_agent = Agent[ECommerceAgentContext](
    name="Triage Agent",
    model="gpt-4.1",
    handoff_description="A order triage agent that can delegate a customer's request to the appropriate agent.",
    instructions=triage_agent_instructions,
    tools=[validate_user],
    handoffs=[
        order_status_agent,
        return_agent,
        handoff(agent=product_faq_agent, on_handoff=on_product_faq_handoff),
        discount_agent,
        payment_agent,
    ],
    input_guardrails=[relevance_guardrail, jailbreak_guardrail],
)