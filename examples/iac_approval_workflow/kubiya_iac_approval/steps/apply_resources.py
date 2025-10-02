import json

from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.utils.terraform import run_terraform_operation


def apply_resources_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    if current_state.approval_status != "approved" and current_state.approval_status != "auto_approved":
        raise ValueError(f"Cannot apply resources. Approval status: {current_state.approval_status}")
    success, apply_output, tf_state = run_terraform_operation(current_state.tf_files, "apply")
    if not success:
        raise ValueError(f"Failed to apply Terraform: {apply_output}")
    current_state.tf_state = json.dumps(tf_state)
    return current_state.dict()
