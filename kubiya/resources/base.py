"""
Base service class for all Kubiya SDK services
"""

from abc import ABC
from typing import Any, Dict, List, Optional, Protocol
from kubiya.resources.exceptions import KubiyaAPIError, ValidationError


class ClientProtocol(Protocol):
    """Protocol defining the interface required by BaseService.

    Any client (KubiyaClient, ControlPlaneClient, etc.) that implements
    a make_request method can be used with BaseService.
    """

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ):
        """Make an HTTP request to the API"""
        ...


class BaseService(ABC):
    """Base class for all service classes"""

    def __init__(self, client: ClientProtocol):
        """
        Initialize base service

        Args:
            client: Client instance that implements make_request method
        """
        self.client = client
    
    def _handle_list_response(
        self, 
        response: Dict[str, Any]
    ) -> List[Any]:
        """Handle list response and convert items"""
        if 'items' in response:
            items_data = response['items']
        elif isinstance(response, list):
            items_data = response
        else:
            # Assume the response itself contains the items
            items_data = response.get('data', [])
        
        if not isinstance(items_data, list):
            raise KubiyaAPIError("Expected list response format")
        
        return items_data
    
    def _format_endpoint(self, endpoint_template: str, **kwargs) -> str:
        """Format endpoint template with parameters"""
        try:
            return endpoint_template.format(**kwargs)
        except KeyError as e:
            raise ValidationError(f"Missing parameter for endpoint: {e}")
    
    def _stream_request(self, method: str, endpoint: str, **kwargs):
        """Make streaming request"""
        return self.client.make_request(method=method, endpoint=endpoint, stream=True, **kwargs)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs):
        """Make GET request"""
        return self.client.make_request(method="GET", endpoint=endpoint, params=params, **kwargs)

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        """Make POST request"""
        return self.client.make_request(method="POST", endpoint=endpoint, data=data, **kwargs)

    def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        """Make PUT request"""
        return self.client.make_request(method="PUT", endpoint=endpoint, data=data, **kwargs)

    def _delete(self, endpoint: str, **kwargs):
        """Make DELETE request"""
        return self.client.make_request(method="DELETE", endpoint=endpoint, **kwargs)

    def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        """Make PATCH request"""
        return self.client.make_request(method="PATCH", endpoint=endpoint, data=data, **kwargs)
