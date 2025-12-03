"""Agents service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import AgentError


class AgentsService(BaseService):
    """Service for agent management and execution in Control Plane"""

    def list(self, skip: int = 0, limit: int = 100, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all agents in the organization.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return
            status_filter: Optional status filter

        Returns:
            List of agent dictionaries

        Raises:
            AgentError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if status_filter:
                params["status_filter"] = status_filter
            response = self._get(ControlPlaneEndpoints.AGENTS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to list agents: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, agent_id: str) -> Dict[str, Any]:
        """
        Get a specific agent by ID.

        Args:
            agent_id: Agent UUID

        Returns:
            Dictionary containing agent details

        Raises:
            AgentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.AGENTS_GET, agent_id=agent_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to get agent {agent_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new agent.

        Args:
            agent_data: Dictionary containing agent configuration

        Returns:
            Dictionary containing created agent details

        Raises:
            AgentError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.AGENTS_CREATE, data=agent_data)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to create agent: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, agent_id: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing agent.

        Args:
            agent_id: Agent UUID
            agent_data: Dictionary containing updated agent configuration

        Returns:
            Dictionary containing updated agent details

        Raises:
            AgentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.AGENTS_UPDATE, agent_id=agent_id)
            response = self._patch(endpoint, data=agent_data)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to update agent {agent_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, agent_id: str) -> Dict[str, Any]:
        """
        Delete an agent.

        Args:
            agent_id: Agent UUID

        Returns:
            Dictionary containing deletion status

        Raises:
            AgentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.AGENTS_DELETE, agent_id=agent_id)
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to delete agent {agent_id}: {str(e)}")
            capture_exception(error)
            raise error

    def execute(
        self,
        agent_id: str,
        execution_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an agent via Temporal workflow.

        Args:
            agent_id: Agent UUID
            execution_data: Execution request data

        Returns:
            Dictionary containing execution details

        Raises:
            AgentError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.AGENTS_EXECUTE, agent_id=agent_id)
            response = self._post(endpoint, data=execution_data)
            return response.json()
        except Exception as e:
            error = AgentError(f"Failed to execute agent {agent_id}: {str(e)}")
            capture_exception(error)
            raise error
