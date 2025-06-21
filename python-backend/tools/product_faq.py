from agents import function_tool # type: ignore

@function_tool(
    name_override="get_product_faq",
    description_override="Provides FAQs about a product."
)
async def get_product_faq(product_id: str) -> dict:
    """
    Returns static FAQ info for the given product_id.
    """
    return {
        "size_guide": "Refer to our size chart on the website for measurements.",
        "composition": "algodão 100%",
        "video": "https://example.com/product_video.mp4",
        "reviews": [
            {"user": "Alice", "rating": 5, "comment": "Great quality!"},
            {"user": "Bob", "rating": 4, "comment": "Comfortable but a bit large."}
        ]
    }
