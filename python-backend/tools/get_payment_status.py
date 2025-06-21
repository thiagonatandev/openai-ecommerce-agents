from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext

@function_tool(
    name_override="get_payment_status",
    description_override="Gets the payment status by payment ID."
)
async def get_payment_status(ctx: RunContextWrapper[ECommerceAgentContext], payment_id: str) -> dict:
    """
    Returns static payment status info for the given payment_id.
    """
    ctx.context.payment_id = payment_id
    return {
        "status": "Pendente",
        "method": "PIX",
        "expires_at": "2025-06-20T23:59:00"
    }
