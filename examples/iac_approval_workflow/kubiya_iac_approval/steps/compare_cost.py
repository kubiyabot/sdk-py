from kubiya_iac_approval.models.state import ResourceRequestState
from kubiya_iac_approval.utils.cost_estimation import (
    compare_cost_with_avg,
    get_average_monthly_cost,
)


async def compare_cost_step(state: dict) -> dict:
    current_state = ResourceRequestState(**state)
    comparison_result = compare_cost_with_avg(current_state.estimated_cost)
    average_monthly_cost = get_average_monthly_cost()
    requires_approval = comparison_result == "greater"
    return {
        "requires_approval": requires_approval,
        "average_monthly_cost": average_monthly_cost,
        **current_state.dict(),  # Include all previous state
    }
