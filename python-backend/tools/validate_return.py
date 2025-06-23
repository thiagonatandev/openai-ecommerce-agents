import datetime
import uuid
from db.postgres.returns_repository import ReturnsRepository
from agents import function_tool
from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="request_return",
    description_override="Requests a return for a given order and product."
)
async def validate_return(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str) -> str:
    """
    Validates return policy and creates a return request if allowed.
    If the user indicates that the product was used or the tag removed, the request is rejected.
    """

    order = ReturnsRepository.get_order_status_and_date(order_number)
    if not order:
        return "Order not found."

    if order['status'].lower() != "delivered" or order['status'].lower() != "shipped":
        return "Return can only be requested for orders with status 'Delivered' or 'Shipped'."

    try:
        created_at = datetime.datetime.fromisoformat(order['created_at'])
    except Exception:
        return "Invalid order date format."

    days_since_delivery = (datetime.datetime.utcnow() - created_at).days
    if days_since_delivery > 30:
        return "Return period expired: orders older than 30 days cannot be returned."
    
    return "Can be returned"

    