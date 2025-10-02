from typing import Any, Dict, Optional

from pydantic import BaseModel


class ResourceRequestState(BaseModel):
    request_id: Optional[str] = None
    user_input: str
    purpose: str
    ttl: str
    resource_details: Dict[str, Any] = {}
    tf_files: Dict[str, str] = {}
    tf_plan: str = ""
    estimated_cost: float = 0
    cost_details: Dict[str, Any] = {}
    requires_approval: bool = False
    average_monthly_cost: float = 0
    approval_status: str = ""
    tf_state: str = ""
    slack_thread_ts: str = ""
