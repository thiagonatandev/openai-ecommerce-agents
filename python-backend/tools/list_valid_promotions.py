from typing import List, Dict
from agents import function_tool
from db.postgres.discounts_repository import DiscountsRepository
from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="list_valid_promotions",
    description_override="Lists valid promotions for a given order number"
)
async def list_valid_promotions(ctx: RunContextWrapper[ECommerceAgentContext], order_number: str) -> List[Dict]:
    """
    Returns a list of valid promotions for the given order.
    """
    result = DiscountsRepository.list_valid_promotions_for_order(order_number)
    if result:
        ctx.context.order_number = order_number
        return result
    else:
        return [{"error": "not found"}]
