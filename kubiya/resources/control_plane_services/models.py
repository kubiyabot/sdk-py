"""Models service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import ModelError


class ModelsService(BaseService):
    """Service for managing LLM models in Control Plane"""

    def list(
        self,
        enabled_only: bool = True,
        provider: Optional[str] = None,
        runtime: Optional[str] = None,
        recommended: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all LLM models with optional filtering.

        Args:
            enabled_only: Only return enabled models (default: True)
            provider: Filter by provider name (e.g., 'Anthropic', 'OpenAI')
            runtime: Filter by compatible runtime (e.g., 'claude_code')
            recommended: Filter by recommended status
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            List of model dictionaries

        Raises:
            ModelError: For API errors
        """
        try:
            params = {
                "enabled_only": enabled_only,
                "skip": skip,
                "limit": limit
            }
            if provider:
                params["provider"] = provider
            if runtime:
                params["runtime"] = runtime
            if recommended is not None:
                params["recommended"] = recommended

            response = self._get(ControlPlaneEndpoints.MODELS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to list models: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, model_id: str) -> Dict[str, Any]:
        """
        Get a specific model by ID or value.

        Accepts either the UUID or the model value (e.g., 'kubiya/claude-sonnet-4').

        Args:
            model_id: Model UUID or model value string

        Returns:
            Dictionary containing model details

        Raises:
            ModelError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.MODELS_GET, model_id=model_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to get model {model_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new LLM model.

        Only accessible by authenticated users (org admins recommended).

        Args:
            model_data: Dictionary containing model configuration

        Returns:
            Dictionary containing created model details

        Raises:
            ModelError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.MODELS_CREATE, data=model_data)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to create model: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, model_id: str, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing model.

        Args:
            model_id: Model UUID or model value string
            model_data: Dictionary containing updated model configuration

        Returns:
            Dictionary containing updated model details

        Raises:
            ModelError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.MODELS_UPDATE, model_id=model_id)
            response = self._put(endpoint, data=model_data)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to update model {model_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, model_id: str) -> Dict[str, Any]:
        """
        Delete a model.

        Args:
            model_id: Model UUID or model value string

        Returns:
            Dictionary containing deletion status

        Raises:
            ModelError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.MODELS_DELETE, model_id=model_id)
            response = self._delete(endpoint)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to delete model {model_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_default(self) -> Dict[str, Any]:
        """
        Get the default recommended LLM model.

        Returns the first model marked as recommended and enabled.
        If none found, returns the first enabled model.

        Returns:
            Dictionary containing default model details

        Raises:
            ModelError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.MODELS_DEFAULT)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to get default model: {str(e)}")
            capture_exception(error)
            raise error

    def list_providers(self) -> List[str]:
        """
        Get list of unique model providers.

        Returns a list of all unique provider names.

        Returns:
            List of provider name strings

        Raises:
            ModelError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.MODELS_PROVIDERS)
            return response.json()
        except Exception as e:
            error = ModelError(f"Failed to list providers: {str(e)}")
            capture_exception(error)
            raise error