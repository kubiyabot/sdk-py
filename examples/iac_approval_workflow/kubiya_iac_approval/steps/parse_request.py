from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.ai.parse_request import parse_user_request


def parse_user_request_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    parsed_request, error_message = parse_user_request(current_state.user_input)
    if error_message:
        raise ValueError("Invalid input")
    current_state.resource_details = parsed_request
    return current_state.model_dump()
