"""Context service for Control Plane API"""

from typing import Dict, Any
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import ControlPlaneError


class ContextService(BaseService):
    """Service for context resolution and management in Control Plane"""

    def get(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        """
        Get context for a specific entity.

        Args:
            entity_type: Type of entity (e.g., 'agent', 'team', 'environment')
            entity_id: ID of the entity

        Returns:
            Dictionary containing entity context

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.CONTEXT_GET,
                entity_type=entity_type,
                entity_id=entity_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to get context for {entity_type} {entity_id}: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, entity_type: str, entity_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update context for a specific entity.

        Args:
            entity_type: Type of entity (e.g., 'agent', 'team', 'environment')
            entity_id: ID of the entity
            context_data: Context data to update

        Returns:
            Dictionary containing updated context

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.CONTEXT_UPDATE,
                entity_type=entity_type,
                entity_id=entity_id
            )
            response = self._put(endpoint, data=context_data)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to update context for {entity_type} {entity_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        """
        Clear/delete context for a specific entity.

        Args:
            entity_type: Type of entity (e.g., 'agent', 'team', 'environment')
            entity_id: ID of the entity

        Returns:
            Dictionary containing deletion status

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.CONTEXT_DELETE,
                entity_type=entity_type,
                entity_id=entity_id
            )
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to delete context for {entity_type} {entity_id}: {str(e)}")
            capture_exception(error)
            raise error

    def resolve(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        """
        Resolve context with inheritance from all layers.

        Args:
            entity_type: Type of entity (e.g., 'agent', 'team', 'environment')
            entity_id: ID of the entity

        Returns:
            Dictionary containing resolved context with inheritance

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.CONTEXT_RESOLVE,
                entity_type=entity_type,
                entity_id=entity_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to resolve context for {entity_type} {entity_id}: {str(e)}")
            capture_exception(error)
            raise error