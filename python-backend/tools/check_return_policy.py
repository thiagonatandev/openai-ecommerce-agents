from agents import function_tool

@function_tool(
    name_override="check_return_policy",
    description_override="Checks the return policy for a product."
)
async def check_return_policy(product_id: str) -> dict:
    """Returns the static example return policy."""
    return {
        "days": 30,
        "exchange_allowed": True,
        "conditions": "produto sem uso e com etiqueta"
    }