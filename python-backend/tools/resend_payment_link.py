from agents import function_tool

@function_tool(
    name_override="resend_payment_link",
    description_override="Resends the payment link for an order."
)
async def resend_payment_link(order_number: str) -> dict:
    """
    Returns a static payment link for the given order number.
    """
    return {
        "payment_link": f"https://pagamento.io/pay/{order_number}"
    }