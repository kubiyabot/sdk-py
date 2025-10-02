import os

from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.utils.approval import schedule_deletion_task


def schedule_deletion_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    if os.getenv("TTL_ENABLED", "true").lower() == "true":
        schedule_deletion_task(current_state.request_id, current_state.ttl, current_state.slack_thread_ts)
    return current_state.dict()
