from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from kubiya.server.app import create_app
from kubiya.tools.models import Arg, Tool
from kubiya.workflows.stateful_workflow import StatefulWorkflow


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def mock_load_workflows_and_tools(source, dynamic_config):
    # Create a workflow with at least one step for testing
    workflow = StatefulWorkflow("TestWorkflow")
    workflow.add_step("test_step", lambda state: {"result": "test"}, "Test step for visualization")

    return {
        "workflows": [{"name": "TestWorkflow", "instance": workflow}],
        "tools": [
            Tool(
                name="TestTool",
                description="A test tool",
                type="python",
                args=[
                    Arg(
                        name="arg1",
                        type="str",
                        description="Test argument",
                        required=True,
                    )
                ],
            )
        ],
    }


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
def test_discover_endpoint(client):
    response = client.post("/discover", json={"source": "/path/to/test/project"})
    assert response.status_code == 200


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
@patch("kubiya.server.routes.run_workflow_with_progress")
def test_run_workflow_endpoint(mock_run_workflow, client):
    mock_run_workflow.return_value = [{"status": "completed"}]
    response = client.post(
        "/run",
        json={
            "source": "/path/to/test/project",
            "name": "TestWorkflow",
            "inputs": {"key": "value"},
        },
    )
    assert response.status_code == 200


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
@patch("kubiya.server.routes.run_tool")
def test_run_tool_endpoint(mock_run_tool, client):
    mock_run_tool.return_value = {"result": "success"}
    response = client.post(
        "/run",
        json={
            "source": "/path/to/test/project",
            "name": "TestTool",
            "inputs": {"arg1": "value"},
        },
    )
    assert response.status_code == 200


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
def test_describe_workflow_endpoint(client):
    response = client.post("/describe", json={"source": "/path/to/test/project", "name": "TestWorkflow"})
    assert response.status_code == 200


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
def test_describe_tool_endpoint(client):
    response = client.post("/describe", json={"source": "/path/to/test/project", "name": "TestTool"})
    assert response.status_code == 200


@patch("kubiya.server.routes.load_workflows_and_tools", mock_load_workflows_and_tools)
def test_visualize_endpoint(client):
    response = client.post(
        "/visualize",
        json={"source": "/path/to/test/project", "workflow": "TestWorkflow"},
    )
    assert response.status_code == 200
