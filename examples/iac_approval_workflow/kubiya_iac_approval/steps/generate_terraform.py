from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.ai.generate_terraform import generate_terraform_code


def generate_terraform_code_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    tf_code_details = generate_terraform_code(current_state.resource_details)
    current_state.tf_files = tf_code_details["tf_files"]
    current_state.resource_details["tf_code_explanation"] = tf_code_details["tf_code_explanation"]
    return current_state.dict()
