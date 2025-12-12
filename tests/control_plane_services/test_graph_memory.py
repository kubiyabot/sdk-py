"""Tests for GraphService memory operation methods"""

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


class TestStoreMemory:
    """Test store_memory method"""

    @patch('requests.Session.request')
    def test_store_memory_basic(self, mock_request, client, mock_response):
        """Test basic memory storage"""
        mock_response.json.return_value = {
            "memory_id": "mem-123",
            "dataset_id": "dataset-456",
            "status": "completed",
            "metadata": {}
        }
        mock_request.return_value = mock_response

        result = client.graph.store_memory(
            dataset_id="dataset-456",
            context="Production deployment completed successfully"
        )

        assert result["memory_id"] == "mem-123"
        assert result["dataset_id"] == "dataset-456"
        assert result["status"] == "completed"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_store_memory_with_metadata(self, mock_request, client, mock_response):
        """Test memory storage with metadata"""
        mock_response.json.return_value = {
            "memory_id": "mem-123",
            "dataset_id": "dataset-456",
            "status": "completed",
            "metadata": {"deployment_id": "deploy-789"}
        }
        mock_request.return_value = mock_response

        result = client.graph.store_memory(
            dataset_id="dataset-456",
            context="Deployment completed",
            metadata={"deployment_id": "deploy-789"}
        )

        assert result["metadata"]["deployment_id"] == "deploy-789"

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["dataset_id"] == "dataset-456"
        assert payload["context"] == "Deployment completed"
        assert payload["metadata"]["deployment_id"] == "deploy-789"

    @patch('requests.Session.request')
    def test_store_memory_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.store_memory(
                dataset_id="dataset-456",
                context="test context"
            )

        assert "Failed to store memory" in str(exc_info.value)


class TestStoreMemoryAsync:
    """Test store_memory_async method"""

    @patch('requests.Session.request')
    def test_store_memory_async_basic(self, mock_request, client, mock_response):
        """Test async memory storage"""
        mock_response.json.return_value = {
            "job_id": "job-123",
            "status": "processing"
        }
        mock_request.return_value = mock_response

        result = client.graph.store_memory_async(
            dataset_id="dataset-456",
            context="Large batch of logs to process"
        )

        assert result["job_id"] == "job-123"
        assert result["status"] == "processing"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_store_memory_async_with_metadata(self, mock_request, client, mock_response):
        """Test async storage with metadata"""
        mock_response.json.return_value = {
            "job_id": "job-456",
            "status": "processing"
        }
        mock_request.return_value = mock_response

        result = client.graph.store_memory_async(
            dataset_id="dataset-789",
            context="Bulk import",
            metadata={"source": "logs"}
        )

        assert result["job_id"] == "job-456"

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["metadata"]["source"] == "logs"


class TestRecallMemory:
    """Test recall_memory method"""

    @patch('requests.Session.request')
    def test_recall_memory_basic(self, mock_request, client, mock_response):
        """Test basic memory recall"""
        mock_response.json.return_value = [
            {
                "memory_id": "mem-1",
                "content": "Recent deployment to production",
                "relevance_score": 0.95,
                "metadata": {"type": "deployment"},
                "created_at": "2023-01-01T00:00:00Z"
            },
            {
                "memory_id": "mem-2",
                "content": "Database migration completed",
                "relevance_score": 0.82,
                "metadata": {"type": "migration"},
                "created_at": "2023-01-02T00:00:00Z"
            }
        ]
        mock_request.return_value = mock_response

        results = client.graph.recall_memory(query="recent deployments")

        assert len(results) == 2
        assert results[0]["memory_id"] == "mem-1"
        assert results[0]["relevance_score"] == 0.95
        assert results[1]["relevance_score"] == 0.82
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_recall_memory_with_limit(self, mock_request, client, mock_response):
        """Test recall with custom limit"""
        mock_response.json.return_value = [
            {"memory_id": f"mem-{i}", "content": f"content {i}", "relevance_score": 0.9}
            for i in range(5)
        ]
        mock_request.return_value = mock_response

        results = client.graph.recall_memory(
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
    def test_recall_specific_memory(self, mock_request, client, mock_response):
        """Test recalling a specific memory by ID"""
        mock_response.json.return_value = [
            {
                "memory_id": "mem-123",
                "content": "Specific memory content",
                "relevance_score": 1.0,
                "metadata": {},
                "created_at": "2023-01-01T00:00:00Z"
            }
        ]
        mock_request.return_value = mock_response

        results = client.graph.recall_memory(
            query="test",
            memory_id="mem-123"
        )

        assert len(results) == 1
        assert results[0]["memory_id"] == "mem-123"

        # Verify memory_id was sent
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["memory_id"] == "mem-123"

    @patch('requests.Session.request')
    def test_recall_memory_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.recall_memory(query="test")

        assert "Failed to recall memory" in str(exc_info.value)


class TestListMemories:
    """Test list_memories method"""

    @patch('requests.Session.request')
    def test_list_memories_basic(self, mock_request, client, mock_response):
        """Test basic memory listing"""
        mock_response.json.return_value = [
            {"memory_id": "mem-1", "content": "Memory 1", "created_at": "2023-01-01T00:00:00Z"},
            {"memory_id": "mem-2", "content": "Memory 2", "created_at": "2023-01-02T00:00:00Z"}
        ]
        mock_request.return_value = mock_response

        results = client.graph.list_memories()

        assert len(results) == 2
        assert results[0]["memory_id"] == "mem-1"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_list_memories_with_pagination(self, mock_request, client, mock_response):
        """Test memory listing with pagination"""
        mock_response.json.return_value = [
            {"memory_id": f"mem-{i}", "content": f"Memory {i}"}
            for i in range(50, 100)
        ]
        mock_request.return_value = mock_response

        results = client.graph.list_memories(skip=50, limit=50)

        assert len(results) == 50
        assert results[0]["memory_id"] == "mem-50"

        # Verify pagination params
        call_kwargs = mock_request.call_args[1]
        params = call_kwargs['params']
        assert params["skip"] == 50
        assert params["limit"] == 50

    @patch('requests.Session.request')
    def test_list_memories_empty(self, mock_request, client, mock_response):
        """Test listing with no memories"""
        mock_response.json.return_value = []
        mock_request.return_value = mock_response

        results = client.graph.list_memories()

        assert len(results) == 0
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_list_memories_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.list_memories()

        assert "Failed to list memories" in str(exc_info.value)
