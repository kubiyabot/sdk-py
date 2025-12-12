"""Dataset management for cognitive datasets"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import GraphError


class DatasetService(BaseService):
    """Service for managing cognitive datasets"""

    def create_dataset(
        self,
        name: str,
        description: Optional[str] = None,
        scope: str = "org",
        allowed_roles: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new cognitive dataset.

        Args:
            name: Dataset name
            description: Optional description
            scope: Visibility scope ("user", "org", "role")
            allowed_roles: List of role IDs if scope="role"

        Returns:
            Dictionary containing dataset details:
            {
                "id": str,
                "name": str,
                "description": str,
                "scope": str,
                "organization_id": str,
                "created_by": str,
                "created_at": str
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> dataset = client.datasets.create_dataset(
            ...     name="production-knowledge",
            ...     description="Production environment context",
            ...     scope="org"
            ... )
        """
        try:
            payload = {
                "name": name,
                "scope": scope
            }
            if description:
                payload["description"] = description
            if allowed_roles:
                payload["allowed_roles"] = allowed_roles

            response = self._post(ControlPlaneEndpoints.DATASETS_CREATE, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to create dataset: {str(e)}")
            capture_exception(error)
            raise error

    def list_datasets(self) -> List[Dict[str, Any]]:
        """
        List all accessible datasets.

        Returns:
            List of dataset dictionaries

        Raises:
            GraphError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.DATASETS_LIST)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list datasets: {str(e)}")
            capture_exception(error)
            raise error

    def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """
        Get dataset details by ID.

        Args:
            dataset_id: Dataset identifier

        Returns:
            Dictionary containing dataset details

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.DATASETS_GET,
                dataset_id=dataset_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get dataset {dataset_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete_dataset(self, dataset_id: str) -> bool:
        """
        Delete a dataset.

        Args:
            dataset_id: Dataset identifier

        Returns:
            True if dataset was deleted successfully

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.DATASETS_DELETE,
                dataset_id=dataset_id
            )
            response = self._delete(endpoint)
            return response.status_code == 204
        except Exception as e:
            error = GraphError(f"Failed to delete dataset {dataset_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_dataset_status(self, dataset_id: str) -> Dict[str, Any]:
        """
        Get dataset processing status.

        Args:
            dataset_id: Dataset identifier

        Returns:
            Dictionary containing dataset status:
            {
                "id": str,
                "status": str,
                "progress": int,
                "message": str
            }

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.DATASETS_STATUS,
                dataset_id=dataset_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get dataset status for {dataset_id}: {str(e)}")
            capture_exception(error)
            raise error
