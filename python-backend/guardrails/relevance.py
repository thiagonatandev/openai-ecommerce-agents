from typing import List, Union
from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail, RunContextWrapper, TResponseInputItem

class RelevanceOutput(BaseModel):
    """Schema for relevance guardrail decisions."""
    reasoning: str
    is_relevant: bool

guardrail_agent = Agent(
    model="gpt-4.1-mini",
    name="Relevance Guardrail",
    instructions=(
        "Determine if the user's message is highly unrelated to a normal customer service "
        "conversation with an e-commerce cs platform (orders, payments, order status, product FAQ, discount, price, etc.). "
        "Important: You are ONLY evaluating the most recent user message, not any of the previous messages from the chat history"
        "It is OK for the customer to send messages such as 'Hi' or 'OK' or any other messages that are at all conversational, "
        "but if the response is non-conversational, it must be somewhat related to e-commerce platform. "
        "Return is_relevant=True if it is, else False, plus a brief reasoning."
    ),
    output_type=RelevanceOutput,
)

@input_guardrail(name="Relevance Guardrail")
async def relevance_guardrail(
    context: RunContextWrapper[None], agent: Agent, input: Union[str, List[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """Guardrail to check if input is relevant to e-commerce topics."""
    result = await Runner.run(guardrail_agent, input, context=context.context)
    final = result.final_output_as(RelevanceOutput)
    return GuardrailFunctionOutput(output_info=final, tripwire_triggered=not final.is_relevant)
