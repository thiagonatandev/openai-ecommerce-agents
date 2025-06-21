from typing import List, Dict, Any
from pydantic import BaseModel
from models.agent_event import AgentEvent
from models.message_response import MessageResponse
from models.guardrail_check import GuardrailCheck

class ChatResponse(BaseModel):
    conversation_id: str
    current_agent: str
    messages: List[MessageResponse]
    events: List[AgentEvent]
    context: Dict[str, Any]
    agents: List[Dict[str, Any]]
    guardrails: List[GuardrailCheck] = []