"""Teams service for Control Plane API"""

from typing import Dict, Any, List, Optional, Iterator, Literal
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import TeamError


class TeamsService(BaseService):
    """Service for managing teams in Control Plane"""

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[Literal['active', 'inactive', 'archived', 'idle']] = None
    ) -> List[Dict[str, Any]]:
        """
        List all teams in the organization.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return
            status_filter: Optional status filter (e.g., 'active', 'inactive')

        Returns:
            List of team dictionaries with agents

        Raises:
            TeamError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if status_filter:
                params["status_filter"] = status_filter
            response = self._get(ControlPlaneEndpoints.TEAMS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to list teams: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, team_id: str) -> Dict[str, Any]:
        """
        Get a specific team by ID.

        Args:
            team_id: Team UUID

        Returns:
            Dictionary containing team details with agents

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.TEAMS_GET, team_id=team_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to get team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new team.

        Args:
            team_data: Dictionary containing team configuration:

        Returns:
            Dictionary containing created team details

        Raises:
            TeamError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.TEAMS_CREATE, data=team_data)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to create team: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, team_id: str, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing team.

        Args:
            team_id: Team UUID
            team_data: Dictionary containing updated team configuration.
                       Only provided fields are updated (partial update).
                - name: Team name
                - description: Team description
                - status: Team status
                - runtime: Runtime type - 'default' or 'claude_code'
                - configuration: Team configuration
                - skill_ids: List of skill IDs
                - skill_configurations: Dict of skill configs
                - environment_ids: List of environment IDs
                - execution_environment: Execution environment config

        Returns:
            Dictionary containing updated team details

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.TEAMS_UPDATE, team_id=team_id)
            response = self._patch(endpoint, data=team_data)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to update team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, team_id: str) -> None:
        """
        Delete a team.

        Args:
            team_id: Team UUID

        Returns:
            None (204 No Content on success)

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.TEAMS_DELETE, team_id=team_id)
            self._delete(endpoint)
        except Exception as e:
            error = TeamError(f"Failed to delete team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def add_agent(self, team_id: str, agent_id: str) -> Dict[str, Any]:
        """
        Add an agent to a team.

        This sets the agent's team_id foreign key. You can also manage members
        through the team's configuration.member_ids field.

        Args:
            team_id: Team UUID
            agent_id: Agent UUID to add

        Returns:
            Dictionary containing updated team details with agents

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.TEAMS_ADD_AGENT,
                team_id=team_id,
                agent_id=agent_id
            )
            response = self._post(endpoint, data={})
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to add agent {agent_id} to team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def remove_agent(self, team_id: str, agent_id: str) -> Dict[str, Any]:
        """
        Remove an agent from a team.

        This clears the agent's team_id foreign key.

        Args:
            team_id: Team UUID
            agent_id: Agent UUID to remove

        Returns:
            Dictionary containing updated team details with agents

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.TEAMS_REMOVE_AGENT,
                team_id=team_id,
                agent_id=agent_id
            )
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to remove agent {agent_id} from team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def execute(self, team_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a team task by submitting to Temporal workflow.

        This creates an execution record and starts a Temporal workflow.
        The actual execution happens asynchronously on the Temporal worker.

        Args:
            team_id: Team UUID
            execution_data: Dictionary containing execution request

        Returns:
            Dictionary containing execution details

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.TEAMS_EXECUTE, team_id=team_id)
            response = self._post(endpoint, data=execution_data)
            return response.json()
        except Exception as e:
            error = TeamError(f"Failed to execute team {team_id}: {str(e)}")
            capture_exception(error)
            raise error

    def execute_stream(
        self,
        team_id: str,
        execution_data: Dict[str, Any]
    ) -> Iterator[bytes]:
        """
        Execute a team task with streaming response.

        The team leader coordinates and delegates the task to appropriate
        team members. Results are streamed back in real-time.

        Args:
            team_id: Team UUID
            execution_data: Dictionary containing execution request:
                - prompt: The prompt/task to execute (required)
                - system_prompt: Optional system prompt for team coordination
                - stream: Whether to stream the response (should be True)
                - worker_queue_id: Worker queue ID (UUID) to route execution to (required)
                - user_metadata: User attribution metadata (optional)

        Returns:
            Iterator of response chunks (Server-Sent Events)

        Raises:
            TeamError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.TEAMS_EXECUTE_STREAM,
                team_id=team_id
            )
            response = self._stream_request("POST", endpoint, data=execution_data)
            return response.iter_content(chunk_size=None)
        except Exception as e:
            error = TeamError(f"Failed to execute team {team_id} with streaming: {str(e)}")
            capture_exception(error)
            raise error
