import os
import logging
from unittest.mock import AsyncMock, patch

import pytest
from kubiya_iac_approval.main import handle_resource_request
from kubiya_iac_approval.workflows.resource_request import (
    create_resource_request_workflow,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def mock_env_vars():
    original_env = os.environ.copy()
    os.environ.update(
        {
            "APPROVAL_WORKFLOW": "true",
            "KUBIYA_USER_EMAIL": "test@example.com",
            "KUBIYA_AGENT_UUID": "test-agent-uuid",
            "APPROVAL_SLACK_CHANNEL": "test-channel",
            "KUBIYA_USER_ORG": "test-org",
            "KUBIYA_API_KEY": "test-api-key",
        }
    )
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_workflow_steps():
    with (
        patch(
            "kubiya_iac_approval.steps.initialize.initialize_request",
            new_callable=AsyncMock,
        ) as mock_init,
        patch(
            "kubiya_iac_approval.steps.parse_request.parse_user_request_step",
            new_callable=AsyncMock,
        ) as mock_parse,
        patch(
            "kubiya_iac_approval.steps.generate_terraform.generate_terraform_code_step",
            new_callable=AsyncMock,
        ) as mock_generate,
        patch(
            "kubiya_iac_approval.steps.create_plan.create_terraform_plan_step",
            new_callable=AsyncMock,
        ) as mock_plan,
        patch(
            "kubiya_iac_approval.steps.estimate_cost.estimate_cost_step",
            new_callable=AsyncMock,
        ) as mock_estimate,
        patch(
            "kubiya_iac_approval.steps.compare_cost.compare_cost_step",
            new_callable=AsyncMock,
        ) as mock_compare,
        patch(
            "kubiya_iac_approval.steps.request_approval.request_approval_step",
            new_callable=AsyncMock,
        ) as mock_approval,
        patch(
            "kubiya_iac_approval.steps.apply_resources.apply_resources_step",
            new_callable=AsyncMock,
        ) as mock_apply,
        patch(
            "kubiya_iac_approval.steps.schedule_deletion.schedule_deletion_step",
            new_callable=AsyncMock,
        ) as mock_delete,
    ):
        mock_init.return_value = {"request_id": "test-123"}
        mock_parse.return_value = {"parsed_request": "Parsed request"}
        mock_generate.return_value = {"tf_code": "Test Terraform code"}
        mock_plan.return_value = {"tf_plan": "Test Terraform plan"}
        mock_estimate.return_value = {"estimated_cost": 100}
        mock_compare.return_value = {"requires_approval": False}
        mock_approval.return_value = {"approval_status": "approved"}
        mock_apply.return_value = {"applied_resources": "Test resources"}
        mock_delete.return_value = {"deletion_scheduled": True}

        yield {
            "initialize": mock_init,
            "parse": mock_parse,
            "generate": mock_generate,
            "plan": mock_plan,
            "estimate": mock_estimate,
            "compare": mock_compare,
            "approval": mock_approval,
            "apply": mock_apply,
            "delete": mock_delete,
        }


@pytest.mark.asyncio
async def test_end_to_end_workflow(mock_env_vars, mock_workflow_steps):
    logger.info("Starting end-to-end workflow test")
    final_state = await handle_resource_request("Create an EC2 instance", "Testing", "1d")

    assert "request_id" in final_state
    assert "parsed_request" in final_state
    assert "tf_code" in final_state
    assert "tf_plan" in final_state
    assert "estimated_cost" in final_state
    assert "requires_approval" in final_state
    assert "approval_status" in final_state
    assert "applied_resources" in final_state
    assert "deletion_scheduled" in final_state

    logger.info("End-to-end workflow test completed successfully")


@pytest.mark.asyncio
async def test_workflow_without_approval(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow without approval test")
    original_approval_workflow = os.environ.get("APPROVAL_WORKFLOW")
    try:
        os.environ["APPROVAL_WORKFLOW"] = "false"
        mock_workflow_steps["approval"].return_value = {"approval_status": "auto_approved"}

        final_state = await handle_resource_request("Create an EC2 instance", "Testing without approval", "1d")

        mock_workflow_steps["approval"].assert_called_once()

        assert (
            final_state["approval_status"] == "auto_approved"
        ), f"Expected 'auto_approved', but got '{final_state.get('approval_status', 'No status')}'"

        logger.info("Workflow without approval test completed successfully")
    finally:
        if original_approval_workflow is None:
            del os.environ["APPROVAL_WORKFLOW"]
        else:
            os.environ["APPROVAL_WORKFLOW"] = original_approval_workflow


@pytest.mark.asyncio
async def test_workflow_with_high_cost(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with high cost test")
    mock_workflow_steps["estimate"].return_value = {"estimated_cost": 1000}
    mock_workflow_steps["compare"].return_value = {"requires_approval": True}
    mock_workflow_steps["approval"].return_value = {"approval_status": "pending"}
    final_state = await handle_resource_request("Create a large EC2 instance", "Testing high-cost scenario", "1d")
    assert final_state["estimated_cost"] == 1000
    assert final_state["requires_approval"] is True
    assert final_state["approval_status"] == "pending"
    logger.info("Workflow with high cost test completed successfully")


@pytest.mark.asyncio
async def test_workflow_with_custom_ttl(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with custom TTL test")
    custom_ttl = "7d"
    final_state = await handle_resource_request("Create an EC2 instance", "Testing custom TTL", custom_ttl)
    assert final_state["ttl"] == custom_ttl
    logger.info("Workflow with custom TTL test completed successfully")


@pytest.mark.asyncio
async def test_workflow_with_invalid_input(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with invalid input test")
    mock_workflow_steps["parse"].side_effect = ValueError("Invalid input")

    with pytest.raises(ValueError, match="Invalid input"):
        await handle_resource_request("", "Invalid request", "1d")

    logger.info("Workflow with invalid input test completed successfully")


@pytest.mark.asyncio
async def test_workflow_with_terraform_generation_error(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with Terraform generation error test")
    mock_workflow_steps["generate"].side_effect = Exception("Terraform generation error")

    with pytest.raises(Exception, match="Terraform generation error"):
        await handle_resource_request("Create an EC2 instance", "Testing error handling", "1d")

    logger.info("Workflow with Terraform generation error test completed successfully")


@pytest.mark.asyncio
async def test_workflow_with_approval_required(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with approval required test")
    mock_workflow_steps["compare"].return_value = {"requires_approval": True}
    mock_workflow_steps["approval"].return_value = {"approval_status": "pending"}

    final_state = await handle_resource_request("Create a medium EC2 instance", "Testing approval process", "1d")

    assert final_state["requires_approval"] is True
    assert final_state["approval_status"] == "pending"
    logger.info("Workflow with approval required test completed successfully")


@pytest.mark.asyncio
async def test_workflow_with_approval_rejected(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow with approval rejected test")
    mock_workflow_steps["compare"].return_value = {"requires_approval": True}
    mock_workflow_steps["approval"].return_value = {"approval_status": "rejected"}

    final_state = await handle_resource_request("Create a large EC2 instance", "Testing rejection", "1d")

    assert final_state["requires_approval"] is True
    assert final_state["approval_status"] == "rejected"
    assert "applied_resources" not in final_state
    logger.info("Workflow with approval rejected test completed successfully")


@pytest.mark.asyncio
async def test_workflow_state_persistence(mock_env_vars, mock_workflow_steps):
    logger.info("Starting workflow state persistence test")
    final_state = await handle_resource_request("Create an EC2 instance", "Testing state persistence", "1d")

    assert final_state["request_id"] == "test-123"
    assert final_state["parsed_request"] == "Parsed request"
    assert final_state["tf_code"] == "Test Terraform code"
    assert "user_input" in final_state
    assert "purpose" in final_state
    assert "ttl" in final_state
    logger.info("Workflow state persistence test completed successfully")


@pytest.mark.asyncio
async def test_workflow_mermaid_diagram(mock_env_vars):
    logger.info("Starting workflow Mermaid diagram test")
    workflow = create_resource_request_workflow()
    mermaid = workflow.to_mermaid()

    assert "graph TD" in mermaid
    assert 'initialize_request["Initialize Request"]' in mermaid
    assert 'parse_user_request["Parse User Request"]' in mermaid
    assert 'generate_terraform_code["Generate Terraform Code"]' in mermaid
    assert 'create_terraform_plan["Create Terraform Plan"]' in mermaid
    assert 'estimate_cost["Estimate Cost"]' in mermaid
    assert 'compare_cost["Compare with Avg Monthly Cost"]' in mermaid
    assert 'request_approval["Request Approval"]' in mermaid
    assert 'apply_resources["Apply Resources"]' in mermaid
    assert 'schedule_deletion["Schedule Deletion"]' in mermaid
    logger.info("Workflow Mermaid diagram test completed successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
