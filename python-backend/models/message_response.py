from typing import Optional
from pydantic import BaseModel


class MessageResponse(BaseModel):
    content: str
    agent: Optional[str] = None
    role: str