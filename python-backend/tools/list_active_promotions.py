from typing import List, Optional
from agents import function_tool

@function_tool(
    name_override="list_active_promotions",
    description_override="Lists active promotions, optionally filtered by user_id."
)
async def list_active_promotions(user_id: Optional[str] = None) -> List[dict]:
    """
    Returns a static list of active promotions.
    """
    return [
        {
            "discount_code": "PROMO123",
            "description": "20% off on orders above R$100",
            "valid_until": "2025-07-31"
        },
        {
            "discount_code": "PROMO456",
            "description": "Free shipping on orders over R$150",
            "valid_until": "2025-08-15"
        }
    ]