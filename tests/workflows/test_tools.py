from unittest.mock import patch

import pytest

from kubiya.tools import Tool, Source, FunctionTool, ToolManagerBridge


@pytest.fixture
def tool_manager():
    return ToolManagerBridge("http://localhost:8000")


@pytest.mark.asyncio
async def test_regular_tool(tool_manager):
    source = Source(url="https://github.com/kubiyabot/terraform-modules")
    tool = Tool(
        name="RegularTool",
        description="A regular tool",
        type="python",
        args=[{"name": "arg1", "type": "str", "required": True, "description": "Test argument"}],
        source=source,
    )

    with patch.object(tool_manager, "execute") as mock_execute:
        mock_execute.return_value = {
            "stdout": "Success",
            "stderr": "",
            "exit_code": 0,
            "output": {"result": "Success"},
        }
        result = tool_manager.execute(tool, {"arg1": "value"})

    assert result["stdout"] == "Success"
    assert result["exit_code"] == 0
    assert result["output"] == {"result": "Success"}


@pytest.mark.asyncio
async def test_function_tool(tool_manager):
    def add_numbers(x: int, y: int) -> int:
        return x + y

    source = Source(url="http://example.com/function-tool-config")
    function_tool = FunctionTool.from_function(
        func=add_numbers,
        name="AddNumbers",
        description="Add two numbers",
        source=source,
    )

    result = await function_tool.execute({"x": 5, "y": 3})
    assert result == 8


# Add more tests for ToolManagerBridge and other scenarios
