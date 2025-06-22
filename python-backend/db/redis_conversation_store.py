import json
from typing import Optional, Dict, Any, Union
import redis
from db.conversation_store import ConversationStore
from utils.get_env import load_config
from context.ecommerce_context import ECommerceAgentContext  # Import your context model

config = load_config()

class RedisConversationStore(ConversationStore):
    def __init__(self, redis_url: str = f'redis://{config["REDIS_HOST"]}:{config["REDIS_PORT"]}', expiration_seconds: int = 3600):
        self.client = redis.Redis.from_url(redis_url)
        self.expiration_seconds = expiration_seconds  
    
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        data = self.client.get(conversation_id)
        if data is None:
            return None
        return json.loads(data)

    def save(self, conversation_id: str, state: Dict[str, Any]):
        def serialize_obj(obj):
            if isinstance(obj, ECommerceAgentContext):
                return obj.dict()
            elif isinstance(obj, dict):
                return {k: serialize_obj(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize_obj(i) for i in obj]
            else:
                return obj

        serializable_state = serialize_obj(state)
        serialized = json.dumps(serializable_state)
        self.client.set(conversation_id, serialized, ex=self.expiration_seconds)