from agents import function_tool, RunContextWrapper
import random as rnd
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="track_order",
    description_override="Check the status of an order from the order number."
)
async def track_order(ctx: RunContextWrapper[ECommerceAgentContext],order_number: str) -> dict:
    """Check and inform the status of orders."""
    tracking_code = f"BR{rnd.randint(100000000, 999999999)}"
    ctx.context.order_number = order_number
    ctx.context.tracking_code = tracking_code
    return {
        "status": "Em trânsito",
        "estimated_delivery": "2025-06-22",
        "carrier": "Correios",
        "tracking_code": tracking_code
    }
