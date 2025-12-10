"""Projects service for Control Plane API"""

from typing import Dict, Any, List, Optional, Literal
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import ProjectError


class ProjectsService(BaseService):
    """Service for managing projects in Control Plane"""

    def list(
        self,
        status_filter: Optional[Literal['active', 'inactive', 'archived']] = None
    ) -> List[Dict[str, Any]]:
        """
        List all projects in the organization.

        Args:
            status_filter: Optional status filter (e.g., 'active', 'inactive', 'archived')

        Returns:
            List of project dictionaries

        Raises:
            ProjectError: For API errors
        """
        try:
            params = {}
            if status_filter:
                params["status_filter"] = status_filter
            response = self._get(ControlPlaneEndpoints.PROJECTS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to list projects: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, project_id: str) -> Dict[str, Any]:
        """
        Get a specific project by ID.

        Args:
            project_id: Project UUID

        Returns:
            Dictionary containing project details

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.PROJECTS_GET, project_id=project_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to get project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_default(self) -> Dict[str, Any]:
        """
        Get the default project for the organization.

        Creates the default project if it doesn't exist.

        Returns:
            Dictionary containing default project details

        Raises:
            ProjectError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.PROJECTS_DEFAULT)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to get default project: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.

        Args:
            project_data: Dictionary containing project configuration:

        Returns:
            Dictionary containing created project details

        Raises:
            ProjectError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.PROJECTS_CREATE, data=project_data)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to create project: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, project_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing project.

        Args:
            project_id: Project UUID
            project_data: Dictionary containing updated project configuration.
                         Only provided fields are updated (partial update).

        Returns:
            Dictionary containing updated project details

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.PROJECTS_UPDATE, project_id=project_id)
            response = self._patch(endpoint, data=project_data)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to update project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, project_id: str) -> None:
        """
        Delete a project.

        This will cascade delete project-agent and project-team associations.

        Args:
            project_id: Project UUID

        Returns:
            None (204 No Content on success)

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.PROJECTS_DELETE, project_id=project_id)
            self._delete(endpoint)
        except Exception as e:
            error = ProjectError(f"Failed to delete project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def add_agent(
        self,
        project_id: str,
        agent_id: str,
        role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add an agent to a project.

        Args:
            project_id: Project UUID
            agent_id: Agent UUID to add
            role: Optional role for the agent in this project

        Returns:
            Dictionary containing the project-agent association details

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_ADD_AGENT,
                project_id=project_id
            )
            data = {"agent_id": agent_id}
            if role:
                data["role"] = role
            response = self._post(endpoint, data=data)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to add agent {agent_id} to project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def list_agents(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all agents in a project.

        Args:
            project_id: Project UUID

        Returns:
            List of project-agent association dictionaries with nested agent data

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_LIST_AGENTS,
                project_id=project_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to list agents for project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def remove_agent(self, project_id: str, agent_id: str) -> None:
        """
        Remove an agent from a project.

        Args:
            project_id: Project UUID
            agent_id: Agent UUID to remove

        Returns:
            None (204 No Content on success)

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_REMOVE_AGENT,
                project_id=project_id,
                agent_id=agent_id
            )
            self._delete(endpoint)
        except Exception as e:
            error = ProjectError(f"Failed to remove agent {agent_id} from project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def add_team(
        self,
        project_id: str,
        team_id: str,
        role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a team to a project.

        Args:
            project_id: Project UUID
            team_id: Team UUID to add
            role: Optional role for the team in this project

        Returns:
            Dictionary containing the project-team association details

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_ADD_TEAM,
                project_id=project_id
            )
            data = {"team_id": team_id}
            if role:
                data["role"] = role
            response = self._post(endpoint, data=data)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to add team {team_id} to project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def list_teams(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all teams in a project.

        Args:
            project_id: Project UUID

        Returns:
            List of project-team association dictionaries with nested team data

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_LIST_TEAMS,
                project_id=project_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ProjectError(f"Failed to list teams for project {project_id}: {str(e)}")
            capture_exception(error)
            raise error

    def remove_team(self, project_id: str, team_id: str) -> None:
        """
        Remove a team from a project.

        Args:
            project_id: Project UUID
            team_id: Team UUID to remove

        Returns:
            None (204 No Content on success)

        Raises:
            ProjectError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.PROJECTS_REMOVE_TEAM,
                project_id=project_id,
                team_id=team_id
            )
            self._delete(endpoint)
        except Exception as e:
            error = ProjectError(f"Failed to remove team {team_id} from project {project_id}: {str(e)}")
            capture_exception(error)
            raise error
