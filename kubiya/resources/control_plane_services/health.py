"""Health service for Control Plane API"""

from typing import Dict, Any
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import ControlPlaneError


class HealthService(BaseService):
    """Service for checking Control Plane health status"""

    def check(self) -> Dict[str, Any]:
        """
        Basic health check endpoint.

        Returns:
            Dictionary containing health status

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.HEALTH)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to check health: {str(e)}")
            capture_exception(error)
            raise error

    def ready(self) -> Dict[str, Any]:
        """
        Readiness check endpoint.

        Returns:
            Dictionary containing readiness status

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.READY)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to check readiness: {str(e)}")
            capture_exception(error)
            raise error

    def detailed(self) -> Dict[str, Any]:
        """
        Detailed health check with dependency status.

        Checks connectivity to database, Redis, and Temporal.

        Returns:
            Dictionary containing detailed health information including
            database, Redis, and Temporal connectivity status

        Raises:
            ControlPlaneError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.HEALTH_DETAILED)
            return response.json()
        except Exception as e:
            error = ControlPlaneError(f"Failed to get detailed health: {str(e)}")
            capture_exception(error)
            raise error