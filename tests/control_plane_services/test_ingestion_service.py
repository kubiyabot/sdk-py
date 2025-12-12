"""Tests for IngestionService"""

from unittest.mock import Mock, patch
import pytest
from kubiya import ControlPlaneClient
from kubiya.resources.exceptions import GraphError


@pytest.fixture
def client():
    """Create a ControlPlaneClient for testing"""
    return ControlPlaneClient(api_key="test-key")


@pytest.fixture
def mock_response():
    """Create a mock response object"""
    response = Mock()
    response.status_code = 200
    return response


class TestIngestNode:
    """Test ingest_node method"""

    @patch('requests.Session.request')
    def test_ingest_node_basic(self, mock_request, client, mock_response):
        """Test basic node ingestion"""
        mock_response.json.return_value = {
            "success": True,
            "node_id": "user-123",
            "created": True,
            "message": "Node created successfully"
        }
        mock_request.return_value = mock_response

        result = client.ingestion.ingest_node(
            id="user-123",
            labels=["User"],
            properties={"name": "Alice", "email": "alice@example.com"}
        )

        assert result["success"] is True
        assert result["node_id"] == "user-123"
        assert result["created"] is True
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_ingest_node_with_dataset(self, mock_request, client, mock_response):
        """Test node ingestion with dataset ID"""
        mock_response.json.return_value = {
            "success": True,
            "node_id": "server-1",
            "created": True,
            "message": "Node created"
        }
        mock_request.return_value = mock_response

        result = client.ingestion.ingest_node(
            id="server-1",
            labels=["Server", "Production"],
            properties={"hostname": "prod-server-01"},
            dataset_id="dataset-456",
            duplicate_handling="skip"
        )

        assert result["success"] is True

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["id"] == "server-1"
        assert payload["labels"] == ["Server", "Production"]
        assert payload["duplicate_handling"] == "skip"
        assert payload["dataset_id"] == "dataset-456"

    @patch('requests.Session.request')
    def test_ingest_node_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.ingestion.ingest_node(
                id="test",
                labels=["Test"],
                properties={}
            )

        assert "Failed to ingest node" in str(exc_info.value)


class TestIngestNodesBatch:
    """Test ingest_nodes_batch method"""

    @patch('requests.Session.request')
    def test_ingest_nodes_batch_basic(self, mock_request, client, mock_response):
        """Test batch node ingestion"""
        mock_response.json.return_value = {
            "summary": {
                "total": 3,
                "success": 3,
                "failed": 0,
                "skipped": 0
            },
            "results": [
                {"node_id": "user-1", "created": True},
                {"node_id": "user-2", "created": True},
                {"node_id": "user-3", "created": True}
            ],
            "errors": []
        }
        mock_request.return_value = mock_response

        nodes = [
            {"id": "user-1", "labels": ["User"], "properties": {"name": "Alice"}},
            {"id": "user-2", "labels": ["User"], "properties": {"name": "Bob"}},
            {"id": "user-3", "labels": ["User"], "properties": {"name": "Charlie"}}
        ]

        result = client.ingestion.ingest_nodes_batch(nodes=nodes)

        assert result["summary"]["total"] == 3
        assert result["summary"]["success"] == 3
        assert len(result["results"]) == 3
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_ingest_nodes_batch_with_options(self, mock_request, client, mock_response):
        """Test batch ingestion with options"""
        mock_response.json.return_value = {
            "summary": {"total": 2, "success": 1, "failed": 0, "skipped": 1},
            "results": [],
            "errors": []
        }
        mock_request.return_value = mock_response

        nodes = [
            {"id": "node-1", "labels": ["Test"], "properties": {}},
            {"id": "node-2", "labels": ["Test"], "properties": {}}
        ]

        result = client.ingestion.ingest_nodes_batch(
            nodes=nodes,
            dataset_id="dataset-123",
            duplicate_handling="skip",
            transactional=True
        )

        assert result["summary"]["skipped"] == 1

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["nodes"] == nodes
        assert payload["dataset_id"] == "dataset-123"
        assert payload["duplicate_handling"] == "skip"
        assert payload["transactional"] is True

    @patch('requests.Session.request')
    def test_ingest_nodes_batch_with_errors(self, mock_request, client, mock_response):
        """Test batch ingestion with errors"""
        mock_response.json.return_value = {
            "summary": {"total": 3, "success": 2, "failed": 1, "skipped": 0},
            "results": [
                {"node_id": "node-1", "created": True},
                {"node_id": "node-2", "created": True}
            ],
            "errors": [
                {"node_id": "node-3", "error": "Invalid property type"}
            ]
        }
        mock_request.return_value = mock_response

        nodes = [
            {"id": "node-1", "labels": ["Test"], "properties": {}},
            {"id": "node-2", "labels": ["Test"], "properties": {}},
            {"id": "node-3", "labels": ["Test"], "properties": {}}
        ]

        result = client.ingestion.ingest_nodes_batch(nodes=nodes)

        assert result["summary"]["failed"] == 1
        assert len(result["errors"]) == 1

    @patch('requests.Session.request')
    def test_ingest_nodes_batch_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.ingestion.ingest_nodes_batch(nodes=[])

        assert "Failed to ingest nodes batch" in str(exc_info.value)


class TestIngestRelationship:
    """Test ingest_relationship method"""

    @patch('requests.Session.request')
    def test_ingest_relationship_basic(self, mock_request, client, mock_response):
        """Test basic relationship ingestion"""
        mock_response.json.return_value = {
            "success": True,
            "relationship_id": "rel-123",
            "created": True
        }
        mock_request.return_value = mock_response

        result = client.ingestion.ingest_relationship(
            source_id="user-1",
            target_id="user-2",
            relationship_type="KNOWS"
        )

        assert result["success"] is True
        assert result["relationship_id"] == "rel-123"
        assert result["created"] is True
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_ingest_relationship_with_properties(self, mock_request, client, mock_response):
        """Test relationship ingestion with properties"""
        mock_response.json.return_value = {
            "success": True,
            "relationship_id": "rel-456",
            "created": True
        }
        mock_request.return_value = mock_response

        result = client.ingestion.ingest_relationship(
            source_id="server-1",
            target_id="database-1",
            relationship_type="CONNECTS_TO",
            properties={"port": 5432, "protocol": "TCP"},
            dataset_id="dataset-789"
        )

        assert result["success"] is True

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["source_id"] == "server-1"
        assert payload["target_id"] == "database-1"
        assert payload["relationship_type"] == "CONNECTS_TO"
        assert payload["properties"]["port"] == 5432
        assert payload["dataset_id"] == "dataset-789"

    @patch('requests.Session.request')
    def test_ingest_relationship_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.ingestion.ingest_relationship(
                source_id="a",
                target_id="b",
                relationship_type="TEST"
            )

        assert "Failed to ingest relationship" in str(exc_info.value)


class TestIngestRelationshipsBatch:
    """Test ingest_relationships_batch method"""

    @patch('requests.Session.request')
    def test_ingest_relationships_batch_basic(self, mock_request, client, mock_response):
        """Test batch relationship ingestion"""
        mock_response.json.return_value = {
            "summary": {
                "total": 2,
                "success": 2,
                "failed": 0,
                "skipped": 0
            },
            "results": [
                {"relationship_id": "rel-1", "created": True},
                {"relationship_id": "rel-2", "created": True}
            ],
            "errors": []
        }
        mock_request.return_value = mock_response

        relationships = [
            {"source_id": "user-1", "target_id": "user-2", "relationship_type": "KNOWS"},
            {"source_id": "user-2", "target_id": "user-3", "relationship_type": "KNOWS"}
        ]

        result = client.ingestion.ingest_relationships_batch(relationships=relationships)

        assert result["summary"]["total"] == 2
        assert result["summary"]["success"] == 2
        assert len(result["results"]) == 2
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_ingest_relationships_batch_with_options(self, mock_request, client, mock_response):
        """Test batch relationship ingestion with options"""
        mock_response.json.return_value = {
            "summary": {"total": 2, "success": 1, "failed": 0, "skipped": 1},
            "results": [],
            "errors": []
        }
        mock_request.return_value = mock_response

        relationships = [
            {"source_id": "a", "target_id": "b", "relationship_type": "TEST"},
            {"source_id": "c", "target_id": "d", "relationship_type": "TEST"}
        ]

        result = client.ingestion.ingest_relationships_batch(
            relationships=relationships,
            dataset_id="dataset-123",
            skip_missing_nodes=True,
            transactional=False
        )

        assert result["summary"]["skipped"] == 1

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["relationships"] == relationships
        assert payload["dataset_id"] == "dataset-123"
        assert payload["skip_missing_nodes"] is True
        assert payload["transactional"] is False

    @patch('requests.Session.request')
    def test_ingest_relationships_batch_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.ingestion.ingest_relationships_batch(relationships=[])

        assert "Failed to ingest relationships batch" in str(exc_info.value)
