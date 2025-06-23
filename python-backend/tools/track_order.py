from agents import function_tool, RunContextWrapper
import random as rnd
from context.ecommerce_context import ECommerceAgentContext
from db.postgres.orders_repository import OrdersRepository
from api_clients.tracking import Tracking
@function_tool(
    name_override="track_order",
    description_override="Check the status of an order from the order number."
)
async def track_order(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str) -> dict:
    """Check and inform the status of orders."""
    user_id = ctx.context.user_id

    order = OrdersRepository.get_order_by_user_id_and_order_number(user_id, order_number)
    if order:
        ctx.context.order_number = order_number
        ctx.context.tracking_code = order["tracking_code"]
        ctx.context.payment_id = order["payment_id"]
        tracking_content = Tracking.get_tracking_data(order["tracking_code"])
        return {
            "order": {
                "number": order_number,
                "status": order["status"],
                "total_amount": order["total_amount"],
                "discount_code": order["discount_code"],
                "created_at": order["created_at"],
                "payment_id": order["payment_id"],
                "tracking_code": order["tracking_code"]
            },
            "tracking": tracking_content or {"error": "Tracking data not available"}
        }
    else:
        return "Not found"
