from agents import function_tool, RunContextWrapper # type: ignore
from context.ecommerce_context import ECommerceAgentContext 
from db.postgres.customers_repository import CustomersRepository

@function_tool(
    name_override="validate_user",
    description_override="Validates if the user exists by the email."
)

async def validate_user(ctx: RunContextWrapper[ECommerceAgentContext], email: str) -> dict:
    """
    If the user is valid, will get the user data and set, if not, will inform the user.
    """

    row = CustomersRepository.get_customer_by_email(email)
    if row:
        ctx.context.customer_email = email
        ctx.context.user_id = row["user_id"]
        return {"valid": True}
    else:
        return {"valid": False}