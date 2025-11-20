"""Task planning service for Control Plane API"""

from typing import Dict, Any, Generator
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import TaskPlanningError


class TaskPlanningService(BaseService):
    """Service for AI-powered task planning in Control Plane"""

    def plan(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a task plan from a description.

        Args:
            task_description: Description of the task to plan
            context: Optional context dictionary for planning

        Returns:
            Dictionary containing the generated plan

        Raises:
            TaskPlanningError: For API errors
        """
        try:
            data = {"task_description": task_description}
            if context:
                data["context"] = context
            response = self._post(ControlPlaneEndpoints.TASK_PLANNING_PLAN, data=data)
            return response.json()
        except Exception as e:
            error = TaskPlanningError(f"Failed to generate task plan: {str(e)}")
            capture_exception(error)
            raise error

    def plan_stream(self, task_description: str, context: Dict[str, Any] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Generate a task plan with streaming updates.

        Args:
            task_description: Description of the task to plan
            context: Optional context dictionary for planning

        Yields:
            Plan generation updates as dictionaries

        Raises:
            TaskPlanningError: For API errors
        """
        try:
            data = {"task_description": task_description}
            if context:
                data["context"] = context
            response = self._stream_request("POST", ControlPlaneEndpoints.TASK_PLANNING_PLAN_STREAM, data=data)

            # Process streaming response
            for line in response.iter_lines():
                if line:
                    if isinstance(line, bytes):
                        line = line.decode("utf-8")
                    # Yield parsed streaming data
                    yield {"data": line}
        except Exception as e:
            error = TaskPlanningError(f"Failed to stream task plan: {str(e)}")
            capture_exception(error)
            raise error
