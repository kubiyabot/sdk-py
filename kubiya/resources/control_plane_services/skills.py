"""Skills service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import SkillError


class SkillsService(BaseService):
    """Service for managing skills/tool sets in Control Plane"""

    def list(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all skills/tool sets.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            List of skill dictionaries

        Raises:
            SkillError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self._get(ControlPlaneEndpoints.SKILLS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to list skills: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, skill_id: str) -> Dict[str, Any]:
        """
        Get a specific skill by ID.

        Args:
            skill_id: Skill UUID

        Returns:
            Dictionary containing skill details

        Raises:
            SkillError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.SKILLS_GET, skill_id=skill_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to get skill {skill_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new skill.

        Args:
            skill_data: Dictionary containing skill configuration

        Returns:
            Dictionary containing created skill details

        Raises:
            SkillError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.SKILLS_CREATE, data=skill_data)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to create skill: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, skill_id: str, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing skill.

        Args:
            skill_id: Skill UUID
            skill_data: Dictionary containing updated skill configuration

        Returns:
            Dictionary containing updated skill details

        Raises:
            SkillError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.SKILLS_UPDATE, skill_id=skill_id)
            response = self._put(endpoint, data=skill_data)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to update skill {skill_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, skill_id: str) -> Dict[str, Any]:
        """
        Delete a skill.

        Args:
            skill_id: Skill UUID

        Returns:
            Dictionary containing deletion status

        Raises:
            SkillError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.SKILLS_DELETE, skill_id=skill_id)
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to delete skill {skill_id}: {str(e)}")
            capture_exception(error)
            raise error

    def associate(self, entity_id: str, skill_ids: List[str]) -> Dict[str, Any]:
        """
        Associate skills with an entity.

        Args:
            entity_id: ID of the entity (agent, team, etc.)
            skill_ids: List of skill IDs to associate

        Returns:
            Dictionary containing association status

        Raises:
            SkillError: For API errors
        """
        try:
            data = {"entity_id": entity_id, "skill_ids": skill_ids}
            response = self._post(ControlPlaneEndpoints.SKILLS_ASSOCIATE, data=data)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to associate skills with entity {entity_id}: {str(e)}")
            capture_exception(error)
            raise error

    def validate(self, skill_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a skill configuration.

        Args:
            skill_config: Dictionary containing skill configuration to validate

        Returns:
            Dictionary containing validation results

        Raises:
            SkillError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.SKILLS_VALIDATE, data=skill_config)
            return response.json()
        except Exception as e:
            error = SkillError(f"Failed to validate skill configuration: {str(e)}")
            capture_exception(error)
            raise error
