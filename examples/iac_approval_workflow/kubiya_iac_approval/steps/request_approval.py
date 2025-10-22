import os
import logging
from datetime import datetime

import requests
from kubiya_iac_approval.models.state import ResourceRequestState

logger = logging.getLogger(__name__)


async def request_approval_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)

    logger.info(f"Starting approval step for request {current_state.request_id}")

    # Check if approval workflow is enabled
    if os.getenv("APPROVAL_WORKFLOW", "").lower() != "true":
        logger.info(f"Approval workflow is disabled. Auto-approving request {current_state.request_id}")
        current_state.approval_status = "auto_approved"
        return current_state.dict()

    # If approval is not required based on previous steps, auto-approve
    if not current_state.requires_approval:
        logger.info(f"Approval not required for request {current_state.request_id}. Auto-approving.")
        current_state.approval_status = "auto_approved"
        return current_state.dict()

    # If we reach here, approval is required
    logger.info(f"Approval required for request {current_state.request_id}. Initiating approval process.")

    prompt = f"""
    You have a new infrastructure resources creation request from {os.getenv('KUBIYA_USER_EMAIL')} for the following purpose: {current_state.purpose}.
    Resource details: {current_state.resource_details}
    The estimated cost for the resource is: ${current_state.estimated_cost}.
    The ID of the request is {current_state.request_id}. Please ask the user if they would like to approve this request or not.
    """

    payload = {
        "agent_id": os.getenv("KUBIYA_AGENT_UUID"),
        "communication": {
            "destination": os.getenv("APPROVAL_SLACK_CHANNEL"),
            "method": "Slack",
        },
        "created_at": datetime.utcnow().isoformat() + "Z",
        "created_by": os.getenv("KUBIYA_USER_EMAIL"),
        "name": "Approval Request",
        "org": os.getenv("KUBIYA_USER_ORG"),
        "prompt": prompt,
        "source": "Triggered by an access request (Agent)",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }

    try:
        logger.info(f"Sending approval request to API for request {current_state.request_id}")
        response = requests.post(
            "https://api.kubiya.ai/api/v1/event",
            headers={
                "Content-Type": "application/json",
                "Authorization": f'UserKey {os.getenv("KUBIYA_API_KEY")}',
            },
            json=payload,
            timeout=30,  # Adding a timeout to prevent indefinite hanging
        )

        if response.status_code < 300:
            logger.info(f"Approval request sent successfully for request {current_state.request_id}")
            current_state.approval_status = "pending"
            event_response = response.json()
            webhook_url = event_response.get("webhook_url")
            if webhook_url:
                logger.info(f"Sending webhook for request {current_state.request_id}")
                webhook_response = requests.post(
                    webhook_url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30,
                )
                if webhook_response.status_code >= 300:
                    logger.error(
                        f"Error sending webhook event for request {current_state.request_id}: {webhook_response.status_code} - {webhook_response.text}"
                    )
                    current_state.error = (
                        f"Error sending webhook event: {webhook_response.status_code} - {webhook_response.text}"
                    )
        else:
            logger.error(
                f"Error requesting approval for request {current_state.request_id}: {response.status_code} - {response.text}"
            )
            current_state.error = f"Error requesting approval: {response.status_code} - {response.text}"
            current_state.approval_status = "error"
    except requests.RequestException as e:
        logger.error(f"Exception in request_approval_step for request {current_state.request_id}: {str(e)}")
        current_state.error = f"Exception in request_approval_step: {str(e)}"
        current_state.approval_status = "error"

    logger.info(
        f"Completed approval step for request {current_state.request_id}. Status: {current_state.approval_status}"
    )
    return current_state.dict()
