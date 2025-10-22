import uuid
from typing import Any, Dict


async def initialize_request(state: Dict[str, Any]) -> Dict[str, Any]:
    state["request_id"] = str(uuid.uuid4())
    return state
