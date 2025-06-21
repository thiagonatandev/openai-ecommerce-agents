from pydantic import BaseModel


class MessageResponse(BaseModel):
    content: str
    agent: str