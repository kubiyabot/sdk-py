"""Runtimes service for Control Plane API"""

from typing import Dict, Any, List
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import RuntimeError


class RuntimesService(BaseService):
    """Service for managing agent runtime types in Control Plane"""

    def list(self) -> List[Dict[str, Any]]:
        """
        List all available agent runtime types.

        Returns:
            List of runtime configuration dictionaries

        Raises:
            RuntimeError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.RUNTIMES_LIST)
            return response.json()
        except Exception as e:
            error = RuntimeError(f"Failed to list runtimes: {str(e)}")
            capture_exception(error)
            raise error

    def get_requirements(self, runtime_id: str) -> Dict[str, Any]:
        """
        Get runtime-specific requirements.

        Args:
            runtime_id: ID of the runtime (e.g., 'claude_code', 'standard')

        Returns:
            Dictionary containing runtime requirements

        Raises:
            RuntimeError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.RUNTIME_REQUIREMENTS, runtime_id=runtime_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = RuntimeError(f"Failed to get requirements for runtime {runtime_id}: {str(e)}")
            capture_exception(error)
            raise error

    def validate(self, runtime_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a runtime configuration.

        Args:
            runtime_config: Dictionary containing runtime configuration to validate

        Returns:
            Dictionary containing validation results

        Raises:
            RuntimeError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.RUNTIME_VALIDATE, data=runtime_config)
            return response.json()
        except Exception as e:
            error = RuntimeError(f"Failed to validate runtime configuration: {str(e)}")
            capture_exception(error)
            raise error