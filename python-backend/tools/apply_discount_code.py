from agents import function_tool, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext 

@function_tool(
    name_override="apply_discount_code",
    description_override="Validates and applies a discount coupon code."
)

async def apply_discount_code(ctx: RunContextWrapper[ECommerceAgentContext], code: str) -> dict:
    """
    Returns static discount code validation and details.
    """
    if ctx.context.discount_code == code:
        return {
        "valid": False,
        "discount_value": "",
        "restrictions": "",
        "reason": "discount already activated"
    }

    ctx.context.discount_code = code
    return {
        "valid": True,
        "discount_value": "20%",
        "restrictions": "válido para compras acima de R$100",
        "reason": ""
    }