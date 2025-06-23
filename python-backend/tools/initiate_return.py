import uuid
from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext
from db.postgres.returns_repository import ReturnsRepository

@function_tool(
    name_override="initiate_return",
    description_override="Initiates a return or exchange request."
)

async def initiate_return(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str, product_id: str, return_reason: str) -> str:
    """Returns the static example return initiation response."""
    ctx.context.return_reason = return_reason
    ctx.context.order_number = order_number
    ctx.context.product_id = product_id

    return_id = str(uuid.uuid4())
    ctx.context.return_reason = return_reason

    ReturnsRepository.create_return(return_id, order_number, product_id, return_reason)
    return f"Return request created successfully. Return ID: {return_id}"



