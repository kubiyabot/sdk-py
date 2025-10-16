import os
import tempfile

from kubiya.utils.discovery import discover_workflows_and_tools
from kubiya.workflows.stateful_workflow import StatefulWorkflow


def create_test_project(base_dir):
    os.makedirs(os.path.join(base_dir, "workflows"))
    with open(os.path.join(base_dir, "workflows", "test_workflow.py"), "w") as f:
        f.write(
            """
from kubiya.workflows.stateful_workflow import StatefulWorkflow

# Create workflow instance at module level for discovery
workflow = StatefulWorkflow("TestWorkflow")

@workflow.step(name="step1")
def step1(state):
    return {"result": state["input"] * 2}
"""
        )

    with open(os.path.join(base_dir, "requirements.txt"), "w") as f:
        f.write("kubiya==1.0.0\n")


def test_discover_workflows_and_tools():
    with tempfile.TemporaryDirectory() as tmpdir:
        create_test_project(tmpdir)

        result = discover_workflows_and_tools(tmpdir)

        assert len(result["workflows"]) == 1
        assert result["workflows"][0]["name"] == "TestWorkflow"
        assert "steps" in result["workflows"][0]
        assert "step1" in result["workflows"][0]["steps"]