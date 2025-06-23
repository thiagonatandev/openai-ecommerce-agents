from agents import RunContextWrapper, function_tool
from db.postgres.orders_repository import OrdersRepository
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="apply_discount_code",
    description_override="Applies a discount code to the given order if valid"
)
async def apply_discount_code(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str, discount_code: str) -> bool:
    """
    Applies the discount code to the order if valid.
    Returns True if applied successfully, False otherwise.
    """
    success = OrdersRepository.apply_discount(order_number, discount_code)
    if success:
        ctx.context.discount_code = discount_code
    return success
