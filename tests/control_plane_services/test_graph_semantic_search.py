"""Tests for GraphService semantic search method"""

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


class TestSemanticSearch:
    """Test semantic_search method"""

    @patch('requests.Session.request')
    def test_semantic_search_basic(self, mock_request, client, mock_response):
        """Test basic semantic search"""
        mock_response.json.return_value = [
            {
                "node_id": "node-1",
                "content": "Production database with high availability",
                "similarity_score": 0.95,
                "metadata": {"type": "database"},
                "source": "cognee"
            },
            {
                "node_id": "node-2",
                "content": "Backup database with replication",
                "similarity_score": 0.87,
                "metadata": {"type": "database"},
                "source": "cognee"
            }
        ]
        mock_request.return_value = mock_response

        results = client.graph.semantic_search(
            query="databases with high availability"
        )

        assert len(results) == 2
        assert results[0]["node_id"] == "node-1"
        assert results[0]["similarity_score"] == 0.95
        assert results[1]["similarity_score"] == 0.87
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_semantic_search_with_limit(self, mock_request, client, mock_response):
        """Test semantic search with custom limit"""
        mock_response.json.return_value = [
            {"node_id": f"node-{i}", "content": f"content {i}", "similarity_score": 0.9}
            for i in range(5)
        ]
        mock_request.return_value = mock_response

        results = client.graph.semantic_search(
            query="test query",
            limit=5
        )

        assert len(results) == 5

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["query"] == "test query"
        assert payload["limit"] == 5

    @patch('requests.Session.request')
    def test_semantic_search_with_filters(self, mock_request, client, mock_response):
        """Test semantic search with filters"""
        mock_response.json.return_value = [
            {
                "node_id": "node-1",
                "content": "AWS EC2 instance",
                "similarity_score": 0.92,
                "metadata": {"integration": "AWS"},
                "source": "cognee"
            }
        ]
        mock_request.return_value = mock_response

        results = client.graph.semantic_search(
            query="EC2 instances",
            limit=10,
            filters={
                "labels": ["EC2Instance"],
                "integration": "AWS"
            }
        )

        assert len(results) == 1
        assert results[0]["metadata"]["integration"] == "AWS"

        # Verify filters were sent
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["filters"]["labels"] == ["EC2Instance"]
        assert payload["filters"]["integration"] == "AWS"

    @patch('requests.Session.request')
    def test_semantic_search_empty_results(self, mock_request, client, mock_response):
        """Test semantic search with no results"""
        mock_response.json.return_value = []
        mock_request.return_value = mock_response

        results = client.graph.semantic_search(query="nonexistent content")

        assert len(results) == 0
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_semantic_search_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.semantic_search(query="test query")

        assert "Failed to perform semantic search" in str(exc_info.value)

    @patch('requests.Session.request')
    def test_semantic_search_ordering(self, mock_request, client, mock_response):
        """Test that results are ordered by similarity score"""
        mock_response.json.return_value = [
            {"node_id": "node-1", "content": "content 1", "similarity_score": 0.95},
            {"node_id": "node-2", "content": "content 2", "similarity_score": 0.90},
            {"node_id": "node-3", "content": "content 3", "similarity_score": 0.85},
        ]
        mock_request.return_value = mock_response

        results = client.graph.semantic_search(query="test")

        # Verify results are in descending order by similarity
        assert results[0]["similarity_score"] >= results[1]["similarity_score"]
        assert results[1]["similarity_score"] >= results[2]["similarity_score"]
