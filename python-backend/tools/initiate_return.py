from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="initiate_return",
    description_override="Initiates a return or exchange request."
)
async def initiate_return(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str, product_id: str, reason: str) -> dict:
    """Returns the static example return initiation response."""
    ctx.context.return_reason = reason
    ctx.context.order_number = order_number
    ctx.context.product_id = product_id
    return {
        "return_id": "RTN7890",
        "label_url": "https://returns.io/label/RTN7890",
        "status": "awaiting dropoff"
    }


