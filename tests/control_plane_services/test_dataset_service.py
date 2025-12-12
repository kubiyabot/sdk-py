"""Tests for DatasetService"""

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


class TestCreateDataset:
    """Test create_dataset method"""

    @patch('requests.Session.request')
    def test_create_dataset_basic(self, mock_request, client, mock_response):
        """Test basic dataset creation"""
        mock_response.json.return_value = {
            "id": "dataset-123",
            "name": "test-dataset",
            "description": None,
            "scope": "org",
            "organization_id": "org-456",
            "created_by": "user-789",
            "created_at": "2023-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response

        result = client.datasets.create_dataset(name="test-dataset")

        assert result["id"] == "dataset-123"
        assert result["name"] == "test-dataset"
        assert result["scope"] == "org"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_create_dataset_with_options(self, mock_request, client, mock_response):
        """Test dataset creation with all options"""
        mock_response.json.return_value = {
            "id": "dataset-456",
            "name": "production-knowledge",
            "description": "Production environment context",
            "scope": "role",
            "allowed_roles": ["admin", "devops"],
            "organization_id": "org-456",
            "created_by": "user-789",
            "created_at": "2023-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response

        result = client.datasets.create_dataset(
            name="production-knowledge",
            description="Production environment context",
            scope="role",
            allowed_roles=["admin", "devops"]
        )

        assert result["id"] == "dataset-456"
        assert result["description"] == "Production environment context"
        assert result["scope"] == "role"
        assert result["allowed_roles"] == ["admin", "devops"]

        # Verify payload
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["name"] == "production-knowledge"
        assert payload["description"] == "Production environment context"
        assert payload["scope"] == "role"
        assert payload["allowed_roles"] == ["admin", "devops"]

    @patch('requests.Session.request')
    def test_create_dataset_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.datasets.create_dataset(name="test")

        assert "Failed to create dataset" in str(exc_info.value)


class TestListDatasets:
    """Test list_datasets method"""

    @patch('requests.Session.request')
    def test_list_datasets_basic(self, mock_request, client, mock_response):
        """Test basic dataset listing"""
        mock_response.json.return_value = [
            {
                "id": "dataset-1",
                "name": "Dataset 1",
                "scope": "org"
            },
            {
                "id": "dataset-2",
                "name": "Dataset 2",
                "scope": "user"
            }
        ]
        mock_request.return_value = mock_response

        results = client.datasets.list_datasets()

        assert len(results) == 2
        assert results[0]["id"] == "dataset-1"
        assert results[1]["scope"] == "user"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_list_datasets_empty(self, mock_request, client, mock_response):
        """Test listing with no datasets"""
        mock_response.json.return_value = []
        mock_request.return_value = mock_response

        results = client.datasets.list_datasets()

        assert len(results) == 0
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_list_datasets_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.datasets.list_datasets()

        assert "Failed to list datasets" in str(exc_info.value)


class TestGetDataset:
    """Test get_dataset method"""

    @patch('requests.Session.request')
    def test_get_dataset_basic(self, mock_request, client, mock_response):
        """Test getting dataset details"""
        mock_response.json.return_value = {
            "id": "dataset-123",
            "name": "test-dataset",
            "description": "Test description",
            "scope": "org",
            "organization_id": "org-456",
            "created_by": "user-789",
            "created_at": "2023-01-01T00:00:00Z"
        }
        mock_request.return_value = mock_response

        result = client.datasets.get_dataset("dataset-123")

        assert result["id"] == "dataset-123"
        assert result["name"] == "test-dataset"
        assert result["description"] == "Test description"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_get_dataset_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.datasets.get_dataset("dataset-123")

        assert "Failed to get dataset dataset-123" in str(exc_info.value)


class TestDeleteDataset:
    """Test delete_dataset method"""

    @patch('requests.Session.request')
    def test_delete_dataset_success(self, mock_request, client):
        """Test successful dataset deletion"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = client.datasets.delete_dataset("dataset-123")

        assert result is True
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_delete_dataset_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.datasets.delete_dataset("dataset-123")

        assert "Failed to delete dataset dataset-123" in str(exc_info.value)


class TestGetDatasetStatus:
    """Test get_dataset_status method"""

    @patch('requests.Session.request')
    def test_get_dataset_status_processing(self, mock_request, client, mock_response):
        """Test getting dataset status during processing"""
        mock_response.json.return_value = {
            "id": "dataset-123",
            "status": "processing",
            "progress": 45,
            "message": "Processing nodes..."
        }
        mock_request.return_value = mock_response

        result = client.datasets.get_dataset_status("dataset-123")

        assert result["id"] == "dataset-123"
        assert result["status"] == "processing"
        assert result["progress"] == 45
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_get_dataset_status_completed(self, mock_request, client, mock_response):
        """Test getting dataset status when completed"""
        mock_response.json.return_value = {
            "id": "dataset-456",
            "status": "completed",
            "progress": 100,
            "message": "All nodes processed successfully"
        }
        mock_request.return_value = mock_response

        result = client.datasets.get_dataset_status("dataset-456")

        assert result["status"] == "completed"
        assert result["progress"] == 100

    @patch('requests.Session.request')
    def test_get_dataset_status_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.datasets.get_dataset_status("dataset-123")

        assert "Failed to get dataset status for dataset-123" in str(exc_info.value)
