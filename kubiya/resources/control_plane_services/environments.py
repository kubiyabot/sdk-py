"""Environments service for Control Plane API"""

from typing import Dict, Any, List, Optional, Literal
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import EnvironmentError


class EnvironmentsService(BaseService):
    """Service for managing environments in Control Plane"""

    def list(
        self,
        status_filter: Optional[Literal['active', 'inactive', 'provisioning', 'ready', 'error']] = None,
    ) -> List[Dict[str, Any]]:
        """
        List all environments in the organization.

        Args:
            status_filter: Optional status filter (e.g., 'active', 'provisioning', 'ready')

        Returns:
            List of environment dictionaries

        Raises:
            EnvironmentError: For API errors
        """
        try:
            params = {}
            if status_filter:
                params["status_filter"] = status_filter
            response = self._get(ControlPlaneEndpoints.ENVIRONMENTS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = EnvironmentError(f"Failed to list environments: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, environment_id: str) -> Dict[str, Any]:
        """
        Get a specific environment by ID.

        Args:
            environment_id: Environment UUID

        Returns:
            Dictionary containing environment details

        Raises:
            EnvironmentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.ENVIRONMENTS_GET,
                environment_id=environment_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = EnvironmentError(f"Failed to get environment {environment_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new environment.

        If this is the first environment for the organization, it will trigger
        Temporal Cloud namespace provisioning workflow.

        Args:
            environment_data: Dictionary containing environment configuration:
                - name: Environment name (required, e.g., 'default', 'production')
                - display_name: User-friendly display name (optional)
                - description: Environment description (optional)
                - tags: List of tags for categorization (optional)
                - settings: Environment settings dict (optional)
                - execution_environment: Execution environment configuration (optional)
                    - env_vars: Dict of environment variables
                    - secrets: List of secret names from Kubiya vault
                    - integration_ids: List of integration UUIDs
                    - mcp_servers: Dict of MCP server configurations

        Returns:
            Dictionary containing created environment details

        Raises:
            EnvironmentError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.ENVIRONMENTS_CREATE, data=environment_data)
            return response.json()
        except Exception as e:
            error = EnvironmentError(f"Failed to create environment: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, environment_id: str, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing environment.

        Args:
            environment_id: Environment UUID
            environment_data: Dictionary containing fields to update. Only provided fields
                             are updated (partial update). Supported fields:
                - name: Environment name
                - display_name: User-friendly display name
                - description: Environment description
                - tags: List of tags
                - settings: Environment settings dict
                - status: Environment status
                - execution_environment: Execution environment configuration

        Returns:
            Dictionary containing updated environment details

        Raises:
            EnvironmentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.ENVIRONMENTS_UPDATE,
                environment_id=environment_id
            )
            response = self._patch(endpoint, data=environment_data)
            return response.json()
        except Exception as e:
            error = EnvironmentError(f"Failed to update environment {environment_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, environment_id: str) -> None:
        """
        Delete an environment.

        Note: Cannot delete the default environment.

        Args:
            environment_id: Environment UUID

        Returns:
            None (204 No Content on success)

        Raises:
            EnvironmentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.ENVIRONMENTS_DELETE,
                environment_id=environment_id
            )
            self._delete(endpoint)
        except Exception as e:
            error = EnvironmentError(f"Failed to delete environment {environment_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_worker_command(self, environment_id: str) -> Dict[str, Any]:
        """
        Get the worker registration command for an environment.

        Returns the kubiya worker start command with the worker token.

        Args:
            environment_id: Environment UUID

        Returns:
            Dictionary containing worker command details:
                - worker_token: Token for worker authentication
                - environment_name: Name of the environment
                - command: Full worker registration command string
                - command_parts: Dict with command components
                - namespace_status: Status of the Temporal namespace
                - can_register: Whether workers can currently register
                - provisioning_workflow_id: Workflow ID if provisioning is in progress

        Raises:
            EnvironmentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.ENVIRONMENTS_WORKER_COMMAND,
                environment_id=environment_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = EnvironmentError(f"Failed to get worker command for environment {environment_id}: {str(e)}")
            capture_exception(error)
            raise error
