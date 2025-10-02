import logging

logger = logging.getLogger(__name__)


def estimate_resource_cost(tf_plan: str) -> tuple[float, dict]:
    # plan = json.loads(tf_plan)
    # This is a placeholder. In a real scenario, you'd use a cost estimation service or library.
    estimated_cost = 10.0  # Example fixed cost
    cost_details = {"hourly_cost": 0.5, "monthly_cost": 360}
    return estimated_cost, cost_details


def compare_cost_with_avg(estimated_cost: float) -> str:
    avg_cost = get_average_monthly_cost()
    if estimated_cost > avg_cost * 1.1:  # 10% threshold
        return "greater"
    return "within_range"


def get_average_monthly_cost() -> float:
    # This is a placeholder. In a real scenario, you'd fetch this from a database or configuration.
    return 300.0
