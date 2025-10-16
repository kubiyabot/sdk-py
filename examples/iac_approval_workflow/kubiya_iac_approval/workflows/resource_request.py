import logging

from pydantic import BaseModel
from kubiya_iac_approval.steps import (
    initialize,
    create_plan,
    compare_cost,
    estimate_cost,
    parse_request,
    apply_resources,
    request_approval,
    schedule_deletion,
    generate_terraform,
)

from kubiya.workflows.stateful_workflow import END, StatefulWorkflow

logger = logging.getLogger(__name__)


class ResourceRequestInput(BaseModel):
    user_input: str
    purpose: str
    ttl: str


def create_resource_request_workflow():
    workflow = StatefulWorkflow(name="ResourceRequestWorkflow", input_schema=ResourceRequestInput)

    workflow.add_step("initialize_request", initialize.initialize_request, "Initialize Request", "📩")
    workflow.add_step(
        "parse_user_request",
        parse_request.parse_user_request_step,
        "Parse User Request",
        "🧠",
    )
    workflow.add_step(
        "generate_terraform_code",
        generate_terraform.generate_terraform_code_step,
        "Generate Terraform Code",
        "🧠",
    )
    workflow.add_step(
        "create_terraform_plan",
        create_plan.create_terraform_plan_step,
        "Create Terraform Plan",
        "🛠️",
    )
    workflow.add_step("estimate_cost", estimate_cost.estimate_cost_step, "Estimate Cost", "💰")
    workflow.add_step(
        "compare_cost",
        compare_cost.compare_cost_step,
        "Compare with Avg Monthly Cost",
        "⚖️",
    )
    workflow.add_step(
        "request_approval",
        request_approval.request_approval_step,
        "Request Approval",
        "🔔",
    )
    workflow.add_step("apply_resources", apply_resources.apply_resources_step, "Apply Resources", "🚀")
    workflow.add_step(
        "schedule_deletion",
        schedule_deletion.schedule_deletion_step,
        "Schedule Deletion",
        "📅",
    )

    workflow.add_edge("initialize_request", "parse_user_request")
    workflow.add_edge("parse_user_request", "generate_terraform_code")
    workflow.add_edge("generate_terraform_code", "create_terraform_plan")
    workflow.add_edge("create_terraform_plan", "estimate_cost")
    workflow.add_edge("estimate_cost", "compare_cost")
    workflow.add_edge("compare_cost", "request_approval")

    workflow.add_condition(
        "request_approval",
        "state['approval_status'] == 'approved' or state['approval_status'] == 'auto_approved'",
        "apply_resources",
    )
    workflow.add_condition(
        "request_approval",
        "state['approval_status'] != 'approved' and state['approval_status'] != 'auto_approved'",
        END,
    )

    workflow.add_edge("apply_resources", "schedule_deletion")
    workflow.add_edge("schedule_deletion", END)

    return workflow


async def handle_resource_request(user_input: str, purpose: str, ttl: str):
    logger.info(f"Handling resource request: {user_input}, Purpose: {purpose}, TTL: {ttl}")
    workflow = create_resource_request_workflow()

    # Diagram of the workflow
    logger.info(f"Workflow diagram:\n{workflow.to_mermaid()}")
    initial_state = ResourceRequestInput(user_input=user_input, purpose=purpose, ttl=ttl)

    try:
        results = await workflow.run(initial_state.dict())
        final_state = results[-1]["state"]
        logger.info(f"Workflow completed. Final state: {final_state}")
        return final_state
    except Exception as e:
        logger.error(f"Error in workflow execution: {str(e)}")
        raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(handle_resource_request("Create an EC2 instance", "Testing", "1d"))
