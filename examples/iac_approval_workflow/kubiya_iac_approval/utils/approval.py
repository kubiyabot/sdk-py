import os
from datetime import datetime, timedelta

import requests
from pytimeparse.timeparse import timeparse


def schedule_deletion_task(request_id: str, ttl: str, slack_thread_ts: str):
    if not os.getenv("RESOURCE_DELETION_ENABLED", "false").lower() == "true":
        print(
            "Resource deletion is not enabled. Please ask the operator who created this task to set the RESOURCE_DELETION_ENABLED environment variable to 'true' to enable it."
        )
        return

    ttl_seconds = timeparse(ttl)
    schedule_time = (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat()

    task_payload = {
        "schedule_time": schedule_time,
        "task_description": f"Delete resources associated with request ID {request_id} as the TTL has expired.",
        "channel_id": os.getenv("NOTIFICATION_CHANNEL_ID")
        or os.getenv("APPROVAL_SLACK_CHANNEL")
        or os.getenv("SLACK_CHANNEL_ID"),
        "user_email": os.getenv("KUBIYA_USER_EMAIL"),
        "organization_name": os.getenv("KUBIYA_USER_ORG"),
        "agent": os.getenv("KUBIYA_AGENT_PROFILE"),
        "thread_ts": slack_thread_ts,
        "request_id": request_id,
    }

    response = requests.post(
        "https://api.kubiya.ai/api/v1/scheduled_tasks",
        headers={
            "Authorization": f'UserKey {os.getenv("KUBIYA_API_KEY")}',
            "Content-Type": "application/json",
        },
        json=task_payload,
    )

    if response.status_code >= 300:
        raise Exception(f"Error scheduling task: {response.status_code} - {response.text}")
    else:
        print(f"Task scheduled successfully for request ID {request_id}.")
