import json

from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.utils.terraform import run_terraform_operation


def create_terraform_plan_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    success, plan_output, plan_json = run_terraform_operation(current_state.tf_files, "plan")
    if not success:
        raise ValueError(f"Failed to create Terraform plan: {plan_output}")
    current_state.tf_plan = json.dumps(plan_json)
    return current_state.dict()
