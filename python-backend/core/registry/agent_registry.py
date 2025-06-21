from ec_agents.triage_agent import triage_agent
from ec_agents.order_status_agent import order_status_agent
from ec_agents.return_agent import return_agent
from ec_agents.product_faq_agent import product_faq_agent
from ec_agents.discount_agent import discount_agent
from ec_agents.payment_agent import payment_agent

order_status_agent.handoffs.append(triage_agent)
return_agent.handoffs.append(triage_agent)
product_faq_agent.handoffs.append(triage_agent)
discount_agent.handoffs.append(triage_agent)
payment_agent.handoffs.append(triage_agent)

AGENTS = {
    a.name: a
    for a in [
        triage_agent,
        order_status_agent,
        return_agent,
        product_faq_agent,
        discount_agent,
        payment_agent,
    ]
}

DEFAULT_AGENT = triage_agent
