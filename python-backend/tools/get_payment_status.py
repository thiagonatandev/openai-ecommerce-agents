from agents import function_tool, RunContextWrapper
from context.ecommerce_context import ECommerceAgentContext
from db.postgres.payments_repository import PaymentsRepository

@function_tool(
    name_override="get_payment_status",
    description_override="Gets the payment status by payment ID."
)
async def get_payment_status(ctx: RunContextWrapper[ECommerceAgentContext], payment_id: str) -> dict:
    """
    Returns static payment status info for the given payment_id.
    """
    
    payment = PaymentsRepository.get_payment_by_id(payment_id)
    if payment:
        ctx.context.payment_id = payment_id
        return {
            "amount": payment["amount"],
            "method:": payment["method"],
            "status": payment["status"],
            "transaction_date": payment["transaction_date"]
        }
    else:
        return None
