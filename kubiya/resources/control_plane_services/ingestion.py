"""Graph data ingestion service"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import GraphError


class IngestionService(BaseService):
    """Service for ingesting nodes and relationships into the graph"""

    def ingest_node(
        self,
        id: str,
        labels: List[str],
        properties: Dict[str, Any],
        dataset_id: Optional[str] = None,
        duplicate_handling: str = "error"
    ) -> Dict[str, Any]:
        """
        Ingest a single node.

        Args:
            id: Node ID
            labels: Node labels (e.g., ["User", "Active"])
            properties: Node properties
            dataset_id: Optional dataset ID for tracking
            duplicate_handling: "error", "skip", "update", or "merge"

        Returns:
            Dictionary containing ingestion result:
            {
                "success": bool,
                "node_id": str,
                "created": bool,
                "message": str
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> result = client.ingestion.ingest_node(
            ...     id="user-123",
            ...     labels=["User"],
            ...     properties={"name": "Alice", "email": "alice@example.com"}
            ... )
        """
        try:
            payload = {
                "id": id,
                "labels": labels,
                "properties": properties,
                "duplicate_handling": duplicate_handling
            }
            if dataset_id:
                payload["dataset_id"] = dataset_id

            params = {}
            if dataset_id:
                params["dataset_id"] = dataset_id

            response = self._post(ControlPlaneEndpoints.INGEST_NODE, data=payload, params=params)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to ingest node: {str(e)}")
            capture_exception(error)
            raise error

    def ingest_nodes_batch(
        self,
        nodes: List[Dict[str, Any]],
        dataset_id: Optional[str] = None,
        duplicate_handling: str = "error",
        transactional: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest multiple nodes in batch (up to 1000).

        Args:
            nodes: List of node dicts with "id", "labels", "properties"
            dataset_id: Optional dataset ID
            duplicate_handling: How to handle duplicates
            transactional: Roll back all if any fail

        Returns:
            Dictionary containing batch results:
            {
                "summary": {
                    "total": int,
                    "success": int,
                    "failed": int,
                    "skipped": int
                },
                "results": List[Dict],
                "errors": List[Dict]
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> nodes = [
            ...     {
            ...         "id": "user-1",
            ...         "labels": ["User"],
            ...         "properties": {"name": "Alice"}
            ...     },
            ...     {
            ...         "id": "user-2",
            ...         "labels": ["User"],
            ...         "properties": {"name": "Bob"}
            ...     }
            ... ]
            >>> result = client.ingestion.ingest_nodes_batch(
            ...     nodes=nodes,
            ...     duplicate_handling="skip"
            ... )
        """
        try:
            payload = {
                "nodes": nodes,
                "duplicate_handling": duplicate_handling,
                "transactional": transactional
            }
            if dataset_id:
                payload["dataset_id"] = dataset_id

            response = self._post(ControlPlaneEndpoints.INGEST_NODES_BATCH, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to ingest nodes batch: {str(e)}")
            capture_exception(error)
            raise error

    def ingest_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
        dataset_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest a single relationship.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Relationship type (e.g., "KNOWS", "MANAGES")
            properties: Optional relationship properties
            dataset_id: Optional dataset ID

        Returns:
            Dictionary containing ingestion result:
            {
                "success": bool,
                "relationship_id": str,
                "created": bool
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> result = client.ingestion.ingest_relationship(
            ...     source_id="user-1",
            ...     target_id="user-2",
            ...     relationship_type="KNOWS",
            ...     properties={"since": "2023"}
            ... )
        """
        try:
            payload = {
                "source_id": source_id,
                "target_id": target_id,
                "relationship_type": relationship_type,
                "properties": properties or {}
            }
            if dataset_id:
                payload["dataset_id"] = dataset_id

            response = self._post(ControlPlaneEndpoints.INGEST_RELATIONSHIP, data=payload)
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to ingest relationship: {str(e)}")
            capture_exception(error)
            raise error

    def ingest_relationships_batch(
        self,
        relationships: List[Dict[str, Any]],
        dataset_id: Optional[str] = None,
        skip_missing_nodes: bool = False,
        transactional: bool = False
    ) -> Dict[str, Any]:
        """
        Ingest multiple relationships in batch.

        Args:
            relationships: List of relationship dicts
            dataset_id: Optional dataset ID
            skip_missing_nodes: Skip if nodes don't exist
            transactional: Roll back all if any fail

        Returns:
            Dictionary containing batch results:
            {
                "summary": {
                    "total": int,
                    "success": int,
                    "failed": int,
                    "skipped": int
                },
                "results": List[Dict],
                "errors": List[Dict]
            }

        Raises:
            GraphError: For API errors

        Example:
            >>> relationships = [
            ...     {
            ...         "source_id": "user-1",
            ...         "target_id": "user-2",
            ...         "relationship_type": "KNOWS"
            ...     },
            ...     {
            ...         "source_id": "user-2",
            ...         "target_id": "user-3",
            ...         "relationship_type": "KNOWS"
            ...     }
            ... ]
            >>> result = client.ingestion.ingest_relationships_batch(
            ...     relationships=relationships,
            ...     skip_missing_nodes=True
            ... )
        """
        try:
            payload = {
                "relationships": relationships,
                "skip_missing_nodes": skip_missing_nodes,
                "transactional": transactional
            }
            if dataset_id:
                payload["dataset_id"] = dataset_id

            response = self._post(
                ControlPlaneEndpoints.INGEST_RELATIONSHIPS_BATCH,
                data=payload
            )
            return response.json()
        except Exception as e:
            error = GraphError(f"Failed to ingest relationships batch: {str(e)}")
            capture_exception(error)
            raise error
