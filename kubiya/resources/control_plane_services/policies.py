"""Policies service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import PolicyError


class PoliciesService(BaseService):
    """Service for managing policies in Control Plane"""

    def list(self, page: int = 1, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all policies.

        Args:
            page: Page for pagination
            limit: Maximum number of records to return

        Returns:
            List of policy dictionaries

        Raises:
            PolicyError: For API errors
        """
        try:
            params = {"page": page, "limit": limit}
            response = self._get(ControlPlaneEndpoints.POLICIES_LIST, params=params)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to list policies: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, policy_id: str) -> Dict[str, Any]:
        """
        Get a specific policy by ID.

        Args:
            policy_id: Policy UUID

        Returns:
            Dictionary containing policy details

        Raises:
            PolicyError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.POLICIES_GET, policy_id=policy_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to get policy {policy_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new policy.

        Args:
            policy_data: Dictionary containing policy configuration

        Returns:
            Dictionary containing created policy details

        Raises:
            PolicyError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.POLICIES_CREATE, data=policy_data)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to create policy: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, policy_id: str, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing policy.

        Args:
            policy_id: Policy UUID
            policy_data: Dictionary containing updated policy configuration

        Returns:
            Dictionary containing updated policy details

        Raises:
            PolicyError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.POLICIES_UPDATE, policy_id=policy_id)
            response = self._put(endpoint, data=policy_data)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to update policy {policy_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, policy_id: str) -> Dict[str, Any]:
        """
        Delete a policy.

        Args:
            policy_id: Policy UUID

        Returns:
            Dictionary containing deletion status

        Raises:
            PolicyError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.POLICIES_DELETE, policy_id=policy_id)
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to delete policy {policy_id}: {str(e)}")
            capture_exception(error)
            raise error

    def evaluate(self, entity_id: str, action: str, resource: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Evaluate a policy for a given entity and action.

        Args:
            entity_id: ID of the entity
            action: Action to evaluate
            resource: Optional resource context

        Returns:
            Dictionary containing evaluation result

        Raises:
            PolicyError: For API errors
        """
        try:
            data = {"entity_id": entity_id, "action": action}
            if resource:
                data["resource"] = resource
            response = self._post(ControlPlaneEndpoints.POLICIES_EVALUATE, data=data)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to evaluate policy for entity {entity_id}: {str(e)}")
            capture_exception(error)
            raise error

    def check_authorization(self, entity_id: str, resource: str, action: str) -> Dict[str, Any]:
        """
        Check if an entity is authorized for an action on a resource.

        Args:
            entity_id: ID of the entity
            resource: Resource identifier
            action: Action to check

        Returns:
            Dictionary containing authorization status

        Raises:
            PolicyError: For API errors
        """
        try:
            data = {"entity_id": entity_id, "resource": resource, "action": action}
            response = self._post(ControlPlaneEndpoints.POLICIES_AUTHORIZE, data=data)
            return response.json()
        except Exception as e:
            error = PolicyError(f"Failed to check authorization for entity {entity_id}: {str(e)}")
            capture_exception(error)
            raise error