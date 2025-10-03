# import pytest
# import tempfile
# import os
# import json
# from click.testing import CliRunner
# from unittest.mock import patch
# from kubiya_sdk.main import cli
# from kubiya_sdk.workflows.stateful_workflow import StatefulWorkflow
# from kubiya_sdk.tools.models import Tool, Arg
# import traceback

# @pytest.fixture
# def runner():
#     return CliRunner()

# @pytest.fixture
# def mock_project():
#     with tempfile.TemporaryDirectory() as tmpdir:
#         # Create a mock workflow file
#         workflow_dir = os.path.join(tmpdir, "workflows")
#         os.makedirs(workflow_dir)
#         with open(os.path.join(workflow_dir, "test_workflow.py"), "w") as f:
#             f.write("""
# from kubiya_sdk.workflows import StatefulWorkflow

# def create_test_workflow():
#     workflow = StatefulWorkflow("TestWorkflow")

#     @workflow.step(name="step1")
#     def step1(state):
#         return {"result": state["input"] * 2}

#     return workflow
# """)

#         # Create a mock tool file
#         tool_dir = os.path.join(tmpdir, "tools")
#         os.makedirs(tool_dir)
#         with open(os.path.join(tool_dir, "test_tool.py"), "w") as f:
#             f.write("""
# from kubiya_sdk.tools import function_tool

# def test_tool(input: int):
#     return {"result": input * 2}

# TestTool = function_tool(test_tool, args=[{"name": "input", "type": "int", "description": "Test input", "required": True}])
# """)

#         yield tmpdir

# def test_discover_command(runner, mock_project):
#     try:
#         result = runner.invoke(cli, ["discover", "--source", mock_project])
#         print("Output:", result.output)
#         print("Exception:", result.exception)
#         print("Exit Code:", result.exit_code)
#         assert result.exit_code == 0
#         assert "TestWorkflow" in result.output
#         assert "TestTool" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise

# @patch("kubiya_sdk.main.run_workflow_with_progress")
# def test_run_workflow_command(mock_run_workflow, runner, mock_project):
#     try:
#         mock_run_workflow.return_value = [{"status": "completed", "result": 10}]

#         with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_input:
#             json.dump({"input": 5}, temp_input)
#             temp_input.flush()

#             result = runner.invoke(cli, [
#                 "run",
#                 "--source", mock_project,
#                 "--name", "TestWorkflow",
#                 "--input", temp_input.name
#             ])
#             print("Output:", result.output)
#             print("Exception:", result.exception)
#             print("Exit Code:", result.exit_code)

#         os.unlink(temp_input.name)

#         assert result.exit_code == 0
#         assert "completed" in result.output
#         assert "10" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise

# @patch("kubiya_sdk.main.run_tool")
# def test_run_tool_command(mock_run_tool, runner, mock_project):
#     try:
#         mock_run_tool.return_value = {"result": 10}

#         with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_input:
#             json.dump({"input": 5}, temp_input)
#             temp_input.flush()

#             result = runner.invoke(cli, [
#                 "run",
#                 "--source", mock_project,
#                 "--name", "TestTool",
#                 "--input", temp_input.name
#             ])
#             print("Output:", result.output)
#             print("Exception:", result.exception)
#             print("Exit Code:", result.exit_code)

#         os.unlink(temp_input.name)

#         assert result.exit_code == 0
#         assert "10" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise

# def test_describe_workflow_command(runner, mock_project):
#     try:
#         result = runner.invoke(cli, [
#             "describe",
#             "--source", mock_project,
#             "--name", "TestWorkflow"
#         ])
#         print("Output:", result.output)
#         print("Exception:", result.exception)
#         print("Exit Code:", result.exit_code)
#         assert result.exit_code == 0
#         assert "TestWorkflow" in result.output
#         assert "step1" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise

# def test_describe_tool_command(runner, mock_project):
#     try:
#         result = runner.invoke(cli, [
#             "describe",
#             "--source", mock_project,
#             "--name", "TestTool"
#         ])
#         print("Output:", result.output)
#         print("Exception:", result.exception)
#         print("Exit Code:", result.exit_code)
#         assert result.exit_code == 0
#         assert "TestTool" in result.output
#         assert "A test tool" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise

# def test_visualize_command(runner, mock_project):
#     try:
#         result = runner.invoke(cli, [
#             "visualize",
#             "--source", mock_project,
#             "--workflow", "TestWorkflow"
#         ])
#         print("Output:", result.output)
#         print("Exception:", result.exception)
#         print("Exit Code:", result.exit_code)
#         assert result.exit_code == 0
#         assert "graph TD" in result.output
#         assert "step1" in result.output
#     except Exception:
#         traceback.print_exc()
#         raise
