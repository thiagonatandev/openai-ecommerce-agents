from typing import List, Optional
import uuid
from pydantic import BaseModel

class Review(BaseModel):
    user: str
    rating: int
    comment: str

class ECommerceAgentContext(BaseModel):
    # Common identifiers
    order_number: Optional[str] = None
    product_id: Optional[str] = None
    customer_email: Optional[str] = None
    tracking_code: Optional[str] = None
    payment_id: Optional[str] = None
    user_id: Optional[str] = None
    discount_code: Optional[str] = None  
    return_reason: Optional[str] = None  

def create_initial_context() -> ECommerceAgentContext:
    ctx = ECommerceAgentContext()
    ctx.user_id = str(uuid.uuid4())
    return ctx
