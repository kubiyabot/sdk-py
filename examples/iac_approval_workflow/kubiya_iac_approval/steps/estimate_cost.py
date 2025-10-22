from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.utils.cost_estimation import estimate_resource_cost


def estimate_cost_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    estimated_cost, cost_details = estimate_resource_cost(current_state.tf_plan)
    current_state.estimated_cost = estimated_cost
    current_state.cost_details = cost_details
    return current_state.dict()
