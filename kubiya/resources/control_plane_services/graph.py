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

    def intelligent_search(
        self,
        keywords: str,
        max_turns: int = 5,
        integration: Optional[str] = None,
        label_filter: Optional[str] = None,
        enable_semantic_search: bool = True,
        enable_cypher_queries: bool = False,
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AI-powered graph search using Claude Agent with graph tools.

        Args:
            keywords: Natural language search query
            max_turns: Maximum conversation turns (1-20, default 5)
            integration: Filter by integration name
            label_filter: Filter by node label
            enable_semantic_search: Enable vector search tool (default True)
            enable_cypher_queries: Allow custom Cypher (default False)
            session_id: Continue existing session (optional)
            temperature: Model creativity 0.0-2.0 (default 0.7)
            model: LiteLLM model identifier (optional)

        Returns:
            Dictionary containing search results:
            {
                "answer": str,
                "nodes": List[Dict],
                "relationships": List[Dict],
                "tool_calls": List[Dict],
                "turns_used": int,
                "confidence": str,
                "suggestions": List[str],
                "session_id": str
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> result = client.graph.intelligent_search(
            ...     keywords="Find all production environments in AWS",
            ...     integration="AWS",
            ...     max_turns=3
            ... )
            >>> print(result["answer"])
            "I found 3 production environments..."
        """
        try:
            payload = {
                "keywords": keywords,
                "max_turns": max_turns,
                "temperature": temperature,
                "enable_semantic_search": enable_semantic_search,
                "enable_cypher_queries": enable_cypher_queries,
            }

            if integration:
                payload["integration"] = integration
            if label_filter:
                payload["label_filter"] = label_filter
            if session_id:
                payload["session_id"] = session_id
            if model:
                payload["model"] = model

            response = self._post(ControlPlaneEndpoints.GRAPH_INTELLIGENT_SEARCH, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to perform intelligent search: {str(e)}")
            capture_exception(error)
            raise error

    def get_search_session(self, session_id: str) -> Dict[str, Any]:
        """
        Get intelligent search session details.

        Args:
            session_id: Session identifier

        Returns:
            Dictionary containing session details:
            {
                "session_id": str,
                "created_at": str,
                "last_accessed": str,
                "turns_used": int,
                "max_turns": int,
                "status": str
            }

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.GRAPH_SEARCH_SESSION,
                session_id=session_id
            )
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to get search session {session_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete_search_session(self, session_id: str) -> bool:
        """
        Delete an intelligent search session.

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted successfully

        Raises:
            GraphError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.GRAPH_SEARCH_SESSION,
                session_id=session_id
            )
            response = self._delete(endpoint)
            return response.status_code == 204
        except Exception as e:
            error = GraphError(f"Failed to delete search session {session_id}: {str(e)}")
            capture_exception(error)
            raise error

    def list_search_sessions(
        self,
        include_expired: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List user's intelligent search sessions.

        Args:
            include_expired: Include expired sessions (default False)

        Returns:
            List of session dictionaries

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"include_expired": include_expired}
            response = self._get(ControlPlaneEndpoints.GRAPH_SEARCH_SESSIONS, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list search sessions: {str(e)}")
            capture_exception(error)
            raise error

    def semantic_search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Natural language semantic search using vector embeddings.

        Args:
            query: Natural language query
            limit: Maximum results (default 10)
            filters: Optional filters (labels, properties, etc.)

        Returns:
            List of nodes with similarity scores:
            [
                {
                    "node_id": str,
                    "content": str,
                    "similarity_score": float,
                    "metadata": Dict,
                    "source": "cognee"
                }
            ]

        Raises:
            GraphError: For API errors

        Example:
            >>> results = client.graph.semantic_search(
            ...     query="databases with high availability",
            ...     limit=5
            ... )
        """
        try:
            payload = {"query": query, "limit": limit}
            if filters:
                payload["filters"] = filters

            response = self._post(ControlPlaneEndpoints.GRAPH_SEMANTIC_SEARCH, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to perform semantic search: {str(e)}")
            capture_exception(error)
            raise error

    def store_memory(
        self,
        dataset_id: str,
        context: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store context in cognitive memory (blocking).

        Args:
            dataset_id: Target dataset ID
            context: Text content to memorize
            metadata: Optional metadata

        Returns:
            Dictionary containing memory details:
            {
                "memory_id": str,
                "dataset_id": str,
                "status": "completed",
                "metadata": Dict
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> memory = client.graph.store_memory(
            ...     dataset_id="prod-knowledge",
            ...     context="Production deployment completed successfully at 2pm"
            ... )
        """
        try:
            payload = {
                "dataset_id": dataset_id,
                "context": context,
                "metadata": metadata or {}
            }
            response = self._post(ControlPlaneEndpoints.GRAPH_MEMORY_STORE, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to store memory: {str(e)}")
            capture_exception(error)
            raise error

    def store_memory_async(
        self,
        dataset_id: str,
        context: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store context in cognitive memory (async, non-blocking).

        Args:
            dataset_id: Target dataset ID
            context: Text content to memorize
            metadata: Optional metadata

        Returns:
            Dictionary containing job details:
            {"job_id": str, "status": "processing"}

        Raises:
            GraphError: For API errors

        Example:
            >>> job = client.graph.store_memory_async(
            ...     dataset_id="prod-knowledge",
            ...     context="Large batch of operational logs"
            ... )
        """
        try:
            payload = {
                "dataset_id": dataset_id,
                "context": context,
                "metadata": metadata or {}
            }
            response = self._post(ControlPlaneEndpoints.GRAPH_MEMORY_STORE_ASYNC, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to store memory asynchronously: {str(e)}")
            capture_exception(error)
            raise error

    def recall_memory(
        self,
        query: str,
        memory_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recall memories matching query.

        Args:
            query: Search query
            memory_id: Optional specific memory ID
            limit: Maximum results

        Returns:
            List of memories with relevance scores:
            [
                {
                    "memory_id": str,
                    "content": str,
                    "relevance_score": float,
                    "metadata": Dict,
                    "created_at": str
                }
            ]

        Raises:
            GraphError: For API errors

        Example:
            >>> memories = client.graph.recall_memory(
            ...     query="recent deployments",
            ...     limit=5
            ... )
        """
        try:
            payload = {"query": query, "limit": limit}
            if memory_id:
                payload["memory_id"] = memory_id

            response = self._post(ControlPlaneEndpoints.GRAPH_MEMORY_RECALL, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to recall memory: {str(e)}")
            capture_exception(error)
            raise error

    def list_memories(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all memories with pagination.

        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return

        Returns:
            List of memory dictionaries

        Raises:
            GraphError: For API errors
        """
        try:
            params = {"skip": skip, "limit": limit}
            response = self._get(ControlPlaneEndpoints.GRAPH_MEMORIES_LIST, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to list memories: {str(e)}")
            capture_exception(error)
            raise error
