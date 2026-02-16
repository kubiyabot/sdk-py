"""Context Graph service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import DataIngestionSourceError


class DataIngestionSourcesService(BaseService):
    """Service for data ingestion sources operations in Control Plane"""

    def list(
        self,
    ) -> Dict[str, Any]:
        """
        Get all data ingestion sources and their schemas available for context graph.

        Returns:
            Dictionary containing a list of data ingestion sources and their schemas

        Raises:
            DataIngestionSourceError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.DATA_INGESTION_SOURCES_LIST)
            return response.json()
        except Exception as e:
            error = DataIngestionSourceError(f"Failed to list data ingestion sources: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, source: str) -> Dict[str, Any]:
        """
        Get a specific source by ID.

        Args:
            source: Source identifier

        Returns:
            Dictionary containing a schema of a particular source

        Raises:
            DataIngestionSourceError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.DATA_INGESTION_SOURCES_GET, integration=source)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = DataIngestionSourceError(f"Failed to get data ingestion source {source}: {str(e)}")
            capture_exception(error)
            raise error

    def validate(self, source: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the given data against the specific source's schema.

        Args:
            source: Source identifier
            data: Data to validate

        Returns:
            Validation errors or a dict with 'valid' key in it

        Raises:
            DataIngestionSourceError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.DATA_INGESTION_SOURCES_VALIDATE, integration=source)
            response = self._post(endpoint, data=data)
            return response.json()
        except Exception as e:
            error = DataIngestionSourceError(f"Failed to validate data ingestion source {source}: {str(e)}")
            capture_exception(error)
            raise error

