"""Workers service for Control Plane API"""

from typing import Dict, Any, List, Optional
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import WorkerError


class WorkersService(BaseService):
    """Service for managing Temporal workers in Control Plane"""

    def list(self) -> List[Dict[str, Any]]:
        """
        List all registered Temporal workers for the organization.

        Returns:
            List of worker/task queue information dictionaries

        Raises:
            WorkerError: For API errors
        """
        try:
            response = self._get(ControlPlaneEndpoints.WORKERS_LIST)
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to list workers: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, runner_name: str) -> Dict[str, Any]:
        """
        Get worker information for a specific runner.

        Args:
            runner_name: Name of the runner

        Returns:
            Dictionary containing worker/task queue information

        Raises:
            WorkerError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.WORKERS_GET, runner_name=runner_name)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to get worker {runner_name}: {str(e)}")
            capture_exception(error)
            raise error

    def register(self, registration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new worker with the control plane.

        Args:
            registration_data: Dictionary containing worker registration details

        Returns:
            Dictionary containing registration response

        Raises:
            WorkerError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.WORKERS_REGISTER, data=registration_data)
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to register worker: {str(e)}")
            capture_exception(error)
            raise error

    def heartbeat(self, heartbeat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send heartbeat from a worker.

        Args:
            heartbeat_data: Dictionary containing worker heartbeat details

        Returns:
            Dictionary containing heartbeat acknowledgment

        Raises:
            WorkerError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.WORKERS_HEARTBEAT, data=heartbeat_data)
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to send worker heartbeat: {str(e)}")
            capture_exception(error)
            raise error

    def heartbeat_simple(self, worker_id: str) -> Dict[str, Any]:
        """
        Send simple heartbeat for a specific worker.

        Args:
            worker_id: Worker identifier

        Returns:
            Dictionary containing heartbeat acknowledgment

        Raises:
            WorkerError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.WORKERS_HEARTBEAT_SIMPLE, worker_id=worker_id)
            response = self._post(endpoint, data={})
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to send simple heartbeat for worker {worker_id}: {str(e)}")
            capture_exception(error)
            raise error

    def start(self, worker_id: str, start_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Start a worker.

        Args:
            worker_id: Worker identifier
            start_data: Optional start configuration

        Returns:
            Dictionary containing start response

        Raises:
            WorkerError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.WORKERS_START, worker_id=worker_id)
            response = self._post(endpoint, data=start_data or {})
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to start worker {worker_id}: {str(e)}")
            capture_exception(error)
            raise error

    def disconnect(self, worker_id: str) -> Dict[str, Any]:
        """
        Disconnect a worker.

        Args:
            worker_id: Worker identifier

        Returns:
            Dictionary containing disconnect response

        Raises:
            WorkerError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.WORKERS_DISCONNECT, worker_id=worker_id)
            response = self._post(endpoint, data={})
            return response.json()
        except Exception as e:
            error = WorkerError(f"Failed to disconnect worker {worker_id}: {str(e)}")
            capture_exception(error)
            raise error