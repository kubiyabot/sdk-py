"""Context Graph service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import GraphError


class GraphService(BaseService):
    """Service for context graph operations in Control Plane"""

    def health(self) -> Dict[str, Any]:
        """
        Check health status of the context graph service.

        Returns:
            Dictionary containing health status

        Raises:
            GraphError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.GRAPH_HEALTH)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to check graph health: {str(e)}")
            capture_exception(error)
            raise error

    def list_nodes(
        self,
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get all nodes in the context graph.

        Args:
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing nodes and count

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._get(ControlPlaneEndpoints.GRAPH_NODES_LIST, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list nodes: {str(e)}")
            capture_exception(error)
            raise error

    def get_node(self, node_id: str, integration: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a specific node by ID.

        Args:
            node_id: Node identifier
            integration: Optional integration filter

        Returns:
            Dictionary containing node details

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.GRAPH_NODES_GET, node_id=node_id)
            params = {"integration": integration} if integration else None
            response = self._get(endpoint, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get node {node_id}: {str(e)}")
            capture_exception(error)
            raise error

    def search_nodes(
        self,
        search_data: Dict[str, Any],
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Search for nodes using structured query.

        Args:
            search_data: Search criteria dictionary
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing matching nodes

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._post(ControlPlaneEndpoints.GRAPH_NODES_SEARCH, data=search_data, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to search nodes: {str(e)}")
            capture_exception(error)
            raise error

    def search_nodes_by_text(
        self,
        text_query: Dict[str, Any],
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Search for nodes using text query.

        Args:
            text_query: Text search query dictionary
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing matching nodes

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._post(ControlPlaneEndpoints.GRAPH_NODES_SEARCH_TEXT, data=text_query, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to search nodes by text: {str(e)}")
            capture_exception(error)
            raise error

    def get_relationships(
        self,
        node_id: str,
        direction: Optional[str] = None,
        relationship_type: Optional[str] = None,
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get relationships for a specific node.

        Args:
            node_id: Node identifier
            direction: Optional direction filter ('incoming', 'outgoing', 'both')
            relationship_type: Optional relationship type filter
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing relationships

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.GRAPH_RELATIONSHIPS, node_id=node_id)
            params = {"skip": skip, "limit": limit}
            if direction:
                params["direction"] = direction
            if relationship_type:
                params["relationship_type"] = relationship_type
            if integration:
                params["integration"] = integration
            response = self._get(endpoint, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get relationships for node {node_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_subgraph(
        self,
        node_id: str,
        depth: int = 1,
        integration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a subgraph starting from a specific node.

        Args:
            node_id: Starting node identifier
            depth: Depth of subgraph traversal (default: 1)
            integration: Optional integration filter

        Returns:
            Dictionary containing subgraph data

        Raises:
            GraphError: For API errors
        """
        try:
            data = {
                "node_id": node_id,
                "depth": depth
            }
            params = {"integration": integration} if integration else None
            response = self._post(ControlPlaneEndpoints.GRAPH_SUBGRAPH, data=data, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get subgraph for node {node_id}: {str(e)}")
            capture_exception(error)
            raise error

    def list_labels(
        self,
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get all labels (node types) in the graph.

        Args:
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing labels

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._get(ControlPlaneEndpoints.GRAPH_LABELS, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list labels: {str(e)}")
            capture_exception(error)
            raise error

    def list_relationship_types(
        self,
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get all relationship types in the graph.

        Args:
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing relationship types

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._get(ControlPlaneEndpoints.GRAPH_RELATIONSHIP_TYPES, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list relationship types: {str(e)}")
            capture_exception(error)
            raise error

    def get_stats(
        self,
        integration: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """c
        Get statistics about the context graph.

        Args:
            integration: Optional integration filter
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing graph statistics

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            if integration:
                params["integration"] = integration
            response = self._get(ControlPlaneEndpoints.GRAPH_STATS, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get graph stats: {str(e)}")
            capture_exception(error)
            raise error

    def execute_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a custom graph query.

        Args:
            query: Graph query dictionary (likely Cypher or similar)

        Returns:
            Dictionary containing query results

        Raises:
            GraphError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.GRAPH_QUERY, data=query)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to execute graph query: {str(e)}")
            capture_exception(error)
            raise error

    def list_integrations(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        Get all integrations available in the context graph.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            Dictionary containing integrations

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self._get(ControlPlaneEndpoints.GRAPH_INTEGRATIONS, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list integrations: {str(e)}")
            capture_exception(error)
            raise error
