"""Secrets service for Control Plane API"""

from typing import Dict, Any, List
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import ControlPlaneError


class SecretsService(BaseService):
    """Service for managing secrets in Control Plane"""

    def list(self) -> List[Dict[str, Any]]:
        """
        List all secrets available in the organization (metadata only, not values).

        Returns:
            List of secret metadata dictionaries

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.SECRETS_LIST)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to list secrets: {str(e)}")
            capture_exception(error)
            raise error

    def get_value(self, name: str) -> Dict[str, Any]:
        """
        Retrieve the actual secret value by name.

        Args:
            name: Name of the secret

        Returns:
            Dictionary containing the secret value

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.SECRETS_VALUE, name=name)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to get secret value for {name}: {str(e)}")
            capture_exception(error)
            raise error