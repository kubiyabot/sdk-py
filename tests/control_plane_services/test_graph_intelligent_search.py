"""Tests for GraphService intelligent search methods"""

from unittest.mock import Mock, patch, MagicMock
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


class TestIntelligentSearch:
    """Test intelligent_search method"""

    @patch('requests.Session.request')
    def test_intelligent_search_basic(self, mock_request, client, mock_response):
        """Test basic intelligent search"""
        mock_response.json.return_value = {
            "answer": "Found 3 production environments",
            "nodes": [
                {"id": "env-1", "properties": {"name": "prod-1"}},
                {"id": "env-2", "properties": {"name": "prod-2"}},
                {"id": "env-3", "properties": {"name": "prod-3"}}
            ],
            "relationships": [],
            "tool_calls": [{"tool": "list_nodes", "params": {}}],
            "turns_used": 2,
            "confidence": "high",
            "suggestions": [],
            "session_id": "abc-123"
        }
        mock_request.return_value = mock_response

        result = client.graph.intelligent_search(keywords="Find production environments")

        assert result["answer"] == "Found 3 production environments"
        assert len(result["nodes"]) == 3
        assert result["session_id"] == "abc-123"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_intelligent_search_with_options(self, mock_request, client, mock_response):
        """Test intelligent search with all options"""
        mock_response.json.return_value = {
            "answer": "Found AWS resources",
            "nodes": [],
            "relationships": [],
            "tool_calls": [],
            "turns_used": 3,
            "confidence": "medium",
            "suggestions": ["Try filtering by label"],
            "session_id": "xyz-456"
        }
        mock_request.return_value = mock_response

        result = client.graph.intelligent_search(
            keywords="Find AWS resources",
            max_turns=10,
            integration="AWS",
            label_filter="EC2Instance",
            enable_semantic_search=True,
            enable_cypher_queries=False,
            temperature=0.5,
            model="claude-3-sonnet"
        )

        assert result["answer"] == "Found AWS resources"
        assert result["turns_used"] == 3
        mock_request.assert_called_once()

        # Verify the payload contains all parameters
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["keywords"] == "Find AWS resources"
        assert payload["max_turns"] == 10
        assert payload["integration"] == "AWS"
        assert payload["label_filter"] == "EC2Instance"
        assert payload["temperature"] == 0.5
        assert payload["model"] == "claude-3-sonnet"

    @patch('requests.Session.request')
    def test_intelligent_search_with_session(self, mock_request, client, mock_response):
        """Test continuing a session"""
        mock_response.json.return_value = {
            "answer": "Here are their dependencies",
            "nodes": [],
            "relationships": [
                {"source": "env-1", "target": "db-1", "type": "CONNECTS_TO"}
            ],
            "tool_calls": [],
            "turns_used": 4,
            "confidence": "high",
            "suggestions": [],
            "session_id": "abc-123"
        }
        mock_request.return_value = mock_response

        result = client.graph.intelligent_search(
            keywords="Show me their dependencies",
            session_id="abc-123"
        )

        assert result["answer"] == "Here are their dependencies"
        assert len(result["relationships"]) == 1

        # Verify session_id was sent
        call_kwargs = mock_request.call_args[1]
        payload = call_kwargs['json']
        assert payload["session_id"] == "abc-123"

    @patch('requests.Session.request')
    def test_intelligent_search_error(self, mock_request, client):
        """Test error handling"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.intelligent_search(keywords="test query")

        assert "Failed to perform intelligent search" in str(exc_info.value)


class TestSearchSessions:
    """Test search session management methods"""

    @patch('requests.Session.request')
    def test_get_search_session(self, mock_request, client, mock_response):
        """Test getting session details"""
        mock_response.json.return_value = {
            "session_id": "abc-123",
            "created_at": "2023-01-01T00:00:00Z",
            "last_accessed": "2023-01-01T00:05:00Z",
            "turns_used": 3,
            "max_turns": 5,
            "status": "active"
        }
        mock_request.return_value = mock_response

        result = client.graph.get_search_session("abc-123")

        assert result["session_id"] == "abc-123"
        assert result["turns_used"] == 3
        assert result["status"] == "active"
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_delete_search_session(self, mock_request, client):
        """Test deleting a session"""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = client.graph.delete_search_session("abc-123")

        assert result is True
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_list_search_sessions(self, mock_request, client, mock_response):
        """Test listing sessions"""
        mock_response.json.return_value = [
            {
                "session_id": "abc-123",
                "created_at": "2023-01-01T00:00:00Z",
                "status": "active"
            },
            {
                "session_id": "xyz-456",
                "created_at": "2023-01-02T00:00:00Z",
                "status": "expired"
            }
        ]
        mock_request.return_value = mock_response

        result = client.graph.list_search_sessions(include_expired=True)

        assert len(result) == 2
        assert result[0]["session_id"] == "abc-123"
        assert result[1]["status"] == "expired"

        # Verify params
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs['params']['include_expired'] is True

    @patch('requests.Session.request')
    def test_list_search_sessions_error(self, mock_request, client):
        """Test error handling for list sessions"""
        mock_request.side_effect = Exception("API Error")

        with pytest.raises(GraphError) as exc_info:
            client.graph.list_search_sessions()

        assert "Failed to list search sessions" in str(exc_info.value)
