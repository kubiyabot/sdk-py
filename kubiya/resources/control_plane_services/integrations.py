"""Integrations service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import IntegrationError


class IntegrationsService(BaseService):
    """Service for managing integrations in Control Plane"""

    def list(self, connected_only: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        List all integrations.

        Args:
            connected_only: If True, only return connected integrations

        Returns:
            List of integration dictionaries

        Raises:
            IntegrationError: For API errors
        """
        try:
            params = {}
            if connected_only is not None:
                params["connected_only"] = connected_only
            response = self._get(ControlPlaneEndpoints.INTEGRATIONS_LIST, params=params if params else None)
            return response.json()
        except Exception as e:
            error = IntegrationError(f"Failed to list integrations: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, integration_id: str) -> Dict[str, Any]:
        """
        Get details for a specific integration.

        Args:
            integration_id: ID of the integration

        Returns:
            Dictionary containing integration details

        Raises:
            IntegrationError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.INTEGRATIONS_GET, integration_id=integration_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = IntegrationError(f"Failed to get integration {integration_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_integration_credentials(self, vendor: str, id: str) -> Dict[str, Any]:
        """
        Get integration credentials by vendor and ID

        Args:
            vendor: Integration vendor name
            id: Integration ID (will be overridden to "0" for special integrations like jira and github_app)

        Returns:
            Dictionary containing integration credentials

        Raises:
            IntegrationError: If API request fails
        """
        try:
            # TODO: special integrations should be handled in a more robust way in v2
            # Special integrations always use ID 0
            SPECIAL_INTEGRATIONS = {"jira", "github_app"}

            # Automatically use "0" for special integrations
            actual_id = "0" if vendor.lower() in SPECIAL_INTEGRATIONS else id

            endpoint = self._format_endpoint(ControlPlaneEndpoints.INTEGRATION_CREDENTIALS, vendor=vendor, id=actual_id)
            response = self._get(endpoint=endpoint)
            return response.json()
        except Exception as e:
            error = IntegrationError(f"Failed to get credentials for integration {vendor}/{id}: {str(e)}")
            capture_exception(error)
            raise error