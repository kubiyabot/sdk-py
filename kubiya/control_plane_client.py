"""Control Plane API client for agent orchestration."""

import json
import requests
from typing import Optional, Dict, Any
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

from kubiya.__version__ import __version__
from kubiya.core.exceptions import (
    APIError as KubiyaAPIError,
    ConnectionError as KubiyaConnectionError,
    WorkflowTimeoutError as KubiyaTimeoutError,
    AuthenticationError as KubiyaAuthenticationError,
)

# Services are imported inside __init__ to avoid circular imports


class ControlPlaneClient:
    """
    Control Plane API client for multi-tenant agent orchestration.

    This client provides access to Control Plane functionality including
    models, runtimes, context resolution, skills, policies, task planning,
    and worker management.

    Example:
        # Initialize with API key
        client = ControlPlaneClient(api_key="your-api-key")

        # List LLM models
        models = client.models.list()

        # Get default model
        default = client.models.get_default()

        # Check health
        health = client.health.check()
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://control-plane.kubiya.ai",
        timeout: int = 300,
        max_retries: int = 3,
        org_name: Optional[str] = None,
    ):
        """
        Initialize Control Plane client

        Args:
            api_key: Kubiya API key
            base_url: Base URL for the Control Plane API (default: https://control-plane.kubiya.ai)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            org_name: Organization name for API calls
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.org_name = org_name

        # Create session with retry logic (same pattern as KubiyaClient)
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers - Use UserKey format (same as KubiyaClient)
        self.session.headers.update({
            "Authorization": f"UserKey {api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"kubiya-control-plane@{__version__}"
        })

        # Initialize all Control Plane services
        from kubiya.resources.control_plane_services import (
            HealthService,
            ModelsService,
            RuntimesService,
            ContextService,
            SkillsService,
            PoliciesService,
            TaskPlanningService,
            AgentsService,
            WorkersService,
            SecretsService,
            IntegrationsService,
            GraphService,
            TeamsService,
            JobsService,
            ProjectsService,
            EnvironmentsService,
        )

        self.health = HealthService(self)
        self.models = ModelsService(self)
        self.runtimes = RuntimesService(self)
        self.context = ContextService(self)
        self.skills = SkillsService(self)
        self.policies = PoliciesService(self)
        self.task_planning = TaskPlanningService(self)
        self.agents = AgentsService(self)
        self.workers = WorkersService(self)
        self.secrets = SecretsService(self)
        self.integrations = IntegrationsService(self)
        self.graph = GraphService(self)
        self.teams = TeamsService(self)
        self.jobs = JobsService(self)
        self.projects = ProjectsService(self)
        self.environments = EnvironmentsService(self)

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Make an HTTP request to the Control Plane API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint path
            data: Request body data (for POST, PUT, PATCH)
            stream: Whether to stream the response
            params: URL query parameters
            **kwargs: Additional request arguments

        Returns:
            Response object

        Raises:
            KubiyaAPIError: For API errors
            KubiyaConnectionError: For connection errors
            KubiyaTimeoutError: For timeout errors
            KubiyaAuthenticationError: For authentication errors
        """
        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
                stream=stream,
                **kwargs,
            )

            # Check for authentication errors
            if response.status_code == 401:
                raise KubiyaAuthenticationError("Invalid API token or unauthorized access")

            # For non-streaming responses, check status
            if not stream:
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except:
                        pass
                    raise KubiyaAPIError(
                        f"API request failed: {e} {error_data}",
                        status_code=response.status_code,
                        response_body=json.dumps(error_data) if error_data else None,
                    )

            return response

        except requests.exceptions.Timeout:
            raise KubiyaTimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise KubiyaConnectionError(f"Failed to connect to Control Plane API: {str(e)}")
        except requests.exceptions.RequestException as e:
            if not isinstance(e, (KubiyaAPIError, KubiyaAuthenticationError)):
                raise KubiyaAPIError(f"Request failed: {str(e)}")
            raise