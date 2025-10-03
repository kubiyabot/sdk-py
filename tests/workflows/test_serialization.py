import json

import pytest

from kubiya_sdk.core.serialization import KubiyaJSONEncoder
from kubiya_sdk.tools.registry import Tool
from kubiya_sdk.workflows.stateful_workflow import StatefulWorkflow


def test_stateful_workflow_serialization():
    workflow = StatefulWorkflow("TestWorkflow")
    workflow.description = "Test workflow description"
    workflow.add_step("step1", lambda x: x, "Step 1 description", "icon1")
    workflow.add_step("step2", lambda x: x, "Step 2 description", "icon2")

    serialized = json.dumps(workflow, cls=KubiyaJSONEncoder)
    deserialized = json.loads(serialized)

    assert deserialized["name"] == "TestWorkflow"
    assert deserialized["description"] == "Test workflow description"
    assert len(deserialized["steps"]) == 2
    assert "step1" in deserialized["steps"]
    assert "step2" in deserialized["steps"]
    assert deserialized["steps"]["step1"]["description"] == "Step 1 description"
    assert deserialized["steps"]["step2"]["icon"] == "icon2"


def test_tool_serialization():
    tool = Tool(name="TestTool", description="Test tool description", type="python")
    tool.args = [
        {
            "name": "arg1",
            "type": str,
            "description": "Arg 1 description",
            "required": True,
        }
    ]
    tool.env = ["ENV_VAR1", "ENV_VAR2"]

    serialized = json.dumps(tool, cls=KubiyaJSONEncoder)
    deserialized = json.loads(serialized)

    assert deserialized["name"] == "TestTool"
    assert deserialized["description"] == "Test tool description"
    assert deserialized["type"] == "python"
    assert len(deserialized["args"]) == 1
    assert deserialized["args"][0]["name"] == "arg1"
    assert deserialized["env"] == ["ENV_VAR1", "ENV_VAR2"]


def test_complex_object_serialization():
    class ComplexObject:
        def __init__(self):
            self.value = "test"

    obj = ComplexObject()

    with pytest.raises(TypeError):
        json.dumps(obj, cls=KubiyaJSONEncoder)


# Add more tests as needed for other serialization scenarios
