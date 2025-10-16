import os

import pytest

from kubiya.tools.registry import Tool, tool_registry
from kubiya.workflows.tool_step import ToolStep
from kubiya.workflows.stateful_workflow import StatefulWorkflow


def test_workflow_creation():
    workflow = StatefulWorkflow("TestWorkflow")
    assert workflow.name == "TestWorkflow"
    assert len(workflow.steps) == 0


def test_add_step():
    workflow = StatefulWorkflow("TestWorkflow")

    @workflow.step(name="step1")
    def step1(state):
        return {"result": state["input"] * 2}

    assert len(workflow.steps) == 1
    assert "step1" in workflow.steps


@pytest.mark.asyncio
async def test_workflow_execution():
    workflow = StatefulWorkflow("TestWorkflow")

    @workflow.step(name="step1")
    def step1(state):
        return {"result": state["input"] * 2}

    @workflow.step(name="step2")
    def step2(state):
        return {"final": state["result"] + 1}

    workflow.add_edge("step1", "step2")

    result = await workflow.run({"input": 5})
    assert result[-1]["state"]["final"] == 11


def test_tool_registration():
    tool = Tool(
        name="TestTool",
        description="A test tool",
        type="python",
        args=[{"name": "input", "type": "int", "required": True, "description": "Input value"}],
    )
    tool_registry.register_tool("test_source", tool)

    assert tool_registry.get_tool("test_source", "TestTool") == tool


def test_tool_step():
    workflow = StatefulWorkflow("ToolWorkflow")

    tool = Tool(
        name="TestTool",
        description="A test tool",
        type="python",
        args=[{"name": "input", "type": "int", "required": True, "description": "Input value"}],
    )
    tool_registry.register_tool("test_source", tool)

    workflow.add_tool_step("tool_step", "TestTool", "test_source")

    assert "tool_step" in workflow.steps
    assert isinstance(workflow.steps["tool_step"], ToolStep)

def test_workflow_to_mermaid():
    workflow = StatefulWorkflow("MermaidWorkflow")

    @workflow.step(name="step1")
    def step1(state):
        return {"result": state["input"] * 2}

    @workflow.step("step2")
    def step2(state):
        return {"final": state["result"] + 1}

    workflow.add_edge("step1", "step2")

    mermaid = workflow.to_mermaid()
    assert "graph TD" in mermaid
    assert "step1" in mermaid
    assert "step2" in mermaid
    assert "step1 --> step2" in mermaid


def test_workflow_from_dict():
    workflow_dict = {
        "name": "DictWorkflow",
        "description": "A workflow created from a dictionary",
        "steps": [
            {"name": "step1", "description": "First step", "next_steps": ["step2"]},
            {
                "name": "step2",
                "description": "Second step",
                "conditions": [
                    {"condition": "state['result'] > 10", "then": "step3"},
                    {"condition": "True", "then": "END"},
                ],
            },
            {"name": "step3", "description": "Third step"},
        ],
    }

    workflow = StatefulWorkflow.from_dict(workflow_dict)

    assert workflow.name == "DictWorkflow"
    assert len(workflow.steps) == 3
    assert "step1" in workflow.steps
    assert "step2" in workflow.steps
    assert "step3" in workflow.steps
    assert workflow.steps["step1"].next_steps == ["step2"]
    assert len(workflow.steps["step2"].conditions) == 2


@pytest.mark.asyncio
async def test_workflow_with_condition():
    workflow = StatefulWorkflow("ConditionalWorkflow")

    @workflow.step(name="step1")
    def step1(state):
        return {"result": state["input"] * 2}

    @workflow.step(name="step2")
    def step2(state):
        return {"final": state["result"] + 10}

    @workflow.step(name="step3")
    def step3(state):
        return {"final": state["result"] + 1}

    workflow.add_edge("step1", "step2")
    workflow.add_condition("step1", "state['result'] > 10", "step3")

    result_high = await workflow.run({"input": 6})
    assert result_high[-1]["state"]["final"] == 13

    result_low = await workflow.run({"input": 4})
    assert result_low[-1]["state"]["final"] == 18


def test_tool_input_validation():
    tool = Tool(
        name="ValidationTool",
        description="A tool with input validation",
        type="python",
        args=[
            {"name": "int_arg", "type": "int", "required": True, "description": "Integer argument"},
            {"name": "str_arg", "type": "str", "required": True, "description": "String argument"},
            {
                "name": "optional_arg",
                "type": "float",
                "required": False,
                "default": 1.0,
                "description": "Optional float argument",
            },
            {
                "name": "enum_arg",
                "type": "str",
                "required": True,
                "options": ["option1", "option2"],
                "description": "Enum argument with options",
            },
        ],
    )

    valid_inputs = {"int_arg": 5, "str_arg": "test", "enum_arg": "option1"}
    assert tool.validate_inputs(valid_inputs) == {
        "int_arg": 5,
        "str_arg": "test",
        "enum_arg": "option1",
        "optional_arg": 1.0,
    }

    with pytest.raises(ValueError, match="Required argument 'int_arg' is missing"):
        tool.validate_inputs({"str_arg": "test", "enum_arg": "option1"})

    with pytest.raises(ValueError, match="Invalid type for argument 'int_arg'. Expected int"):
        tool.validate_inputs({"int_arg": "not an int", "str_arg": "test", "enum_arg": "option1"})

    with pytest.raises(
        ValueError,
        match="Invalid value for argument 'enum_arg'. Must be one of: option1, option2",
    ):
        tool.validate_inputs({"int_arg": 5, "str_arg": "test", "enum_arg": "invalid_option"})


@pytest.mark.asyncio
async def test_workflow_with_env_vars_and_files(tmp_path):
    workflow = StatefulWorkflow("EnvFileWorkflow")

    @workflow.step(name="env_step")
    def env_step(state):
        return {"env_var": os.environ.get("TEST_ENV_VAR")}

    @workflow.step(name="file_step")
    def file_step(state):
        with open("test_file.txt", "r") as f:
            content = f.read()
        return {"file_content": content}

    workflow.add_edge("env_step", "file_step")

    env_vars = {"TEST_ENV_VAR": "test_value"}
    files = {"test_file.txt": "test content"}

    result = await workflow.run({}, env_vars=env_vars, files=files)

    assert result[-1]["state"]["env_var"] == "test_value"
    assert result[-1]["state"]["file_content"] == "test content"


if __name__ == "__main__":
    pytest.main([__file__])
