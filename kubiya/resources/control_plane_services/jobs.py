"""Jobs service for Control Plane API"""

from typing import Dict, Any, List, Optional, Literal
from kubiya import capture_exception
from kubiya.resources.base import BaseService
from kubiya.resources.constants import ControlPlaneEndpoints
from kubiya.resources.exceptions import JobError


class JobsService(BaseService):
    """Service for managing scheduled and webhook-triggered jobs in Control Plane"""

    def list(
        self,
        enabled: Optional[bool] = None,
        trigger_type: Optional[Literal['cron', 'webhook', 'manual']] = None,
    ) -> List[Dict[str, Any]]:
        """
        List all jobs in the organization.

        Args:
            enabled: Filter by enabled status (True/False)
            trigger_type: Filter by trigger type ('cron', 'webhook', 'manual')

        Returns:
            List of job dictionaries

        Raises:
            JobError: For API errors
        """
        try:
            params = {}
            if enabled is not None:
                params["enabled"] = enabled
            if trigger_type:
                params["trigger_type"] = trigger_type
            response = self._get(ControlPlaneEndpoints.JOBS_LIST, params=params)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to list jobs: {str(e)}")
            capture_exception(error)
            raise error

    def get(self, job_id: str) -> Dict[str, Any]:
        """
        Get a specific job by ID.

        Args:
            job_id: Job ID (format: job_<uuid>)

        Returns:
            Dictionary containing job details

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_GET, job_id=job_id)
            response = self._get(endpoint)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to get job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def create(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job.

        Jobs can be triggered via cron schedule, webhook, or manual API trigger.

        Args:
            job_data: Dictionary containing job configuration:
                - name: Job name (required)
                - trigger_type: 'cron', 'webhook', or 'manual' (required)
                - cron_schedule: Cron expression (required for cron trigger)
                - cron_timezone: Timezone for cron schedule (default: 'UTC')
                - planning_mode: 'on_the_fly', 'predefined_agent', 'predefined_team',
                                 or 'predefined_workflow'
                - entity_type: 'agent' or 'team' (for predefined modes)
                - entity_id: Entity UUID (for predefined modes)
                - prompt_template: Prompt template with {{variable}} placeholders
                - system_prompt: Optional system prompt override
                - executor_type: 'auto', 'specific_queue', or 'environment'
                - worker_queue_name: Specific worker queue name
                - environment_name: Environment name for execution
                - config: Additional configuration dict
                - execution_environment: Execution environment config
                - enabled: Whether job is enabled (default: True)
                - description: Optional job description

        Returns:
            Dictionary containing created job details with webhook_url if applicable

        Raises:
            JobError: For API errors
        """
        try:
            response = self._post(ControlPlaneEndpoints.JOBS_CREATE, data=job_data)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to create job: {str(e)}")
            capture_exception(error)
            raise error

    def update(self, job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing job.

        Note: Updating cron_schedule will recreate the Temporal Schedule.

        Args:
            job_id: Job ID
            job_data: Dictionary containing fields to update. Only provided fields
                      are updated (partial update). Supported fields:
                - name: Job name
                - description: Job description
                - enabled: Whether job is enabled
                - cron_schedule: Cron expression
                - cron_timezone: Timezone for cron schedule
                - planning_mode: Planning mode
                - entity_type: Entity type
                - entity_id: Entity ID
                - prompt_template: Prompt template
                - system_prompt: System prompt
                - executor_type: Executor type
                - worker_queue_name: Worker queue name
                - environment_name: Environment name
                - config: Configuration dict
                - execution_environment: Execution environment config

        Returns:
            Dictionary containing updated job details

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_UPDATE, job_id=job_id)
            response = self._patch(endpoint, data=job_data)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to update job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def delete(self, job_id: str) -> None:
        """
        Delete a job and its Temporal Schedule.

        Args:
            job_id: Job ID

        Returns:
            None (204 No Content on success)

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_DELETE, job_id=job_id)
            self._delete(endpoint)
        except Exception as e:
            error = JobError(f"Failed to delete job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def trigger(
        self,
        job_id: str,
        parameters: Optional[Dict[str, Any]] = None,
        config_override: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Manually trigger a job execution.

        Args:
            job_id: Job ID
            parameters: Dictionary of parameters to substitute in prompt template
            config_override: Optional config overrides for this execution

        Returns:
            Dictionary containing trigger response:
                - job_id: Job ID
                - workflow_id: Temporal workflow ID
                - execution_id: Execution UUID
                - status: 'started'
                - message: Success message

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_TRIGGER, job_id=job_id)
            data = {}
            if parameters:
                data["parameters"] = parameters
            if config_override:
                data["config_override"] = config_override
            response = self._post(endpoint, data=data)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to trigger job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def enable(self, job_id: str) -> Dict[str, Any]:
        """
        Enable a job and unpause its Temporal Schedule.

        For cron jobs, this will create the Temporal Schedule if it doesn't exist.

        Args:
            job_id: Job ID

        Returns:
            Dictionary containing updated job details

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_ENABLE, job_id=job_id)
            response = self._post(endpoint, data={})
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to enable job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def disable(self, job_id: str) -> Dict[str, Any]:
        """
        Disable a job and pause its Temporal Schedule.

        Args:
            job_id: Job ID

        Returns:
            Dictionary containing updated job details

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_DISABLE, job_id=job_id)
            response = self._post(endpoint, data={})
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to disable job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def get_executions(
        self,
        job_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        Get execution history for a job.

        Args:
            job_id: Job ID
            limit: Maximum number of executions to return (default: 50)
            offset: Number of executions to skip (default: 0)

        Returns:
            Dictionary containing:
                - job_id: Job ID
                - total_count: Total number of executions
                - executions: List of execution history items with:
                    - execution_id: Execution UUID
                    - trigger_type: Type of trigger
                    - status: Execution status
                    - started_at: Start timestamp
                    - completed_at: Completion timestamp
                    - duration_ms: Duration in milliseconds
                    - error_message: Error message if failed
                    - trigger_metadata: Trigger metadata

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(ControlPlaneEndpoints.JOBS_EXECUTIONS, job_id=job_id)
            params = {"limit": limit, "offset": offset}
            response = self._get(endpoint, params=params)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to get executions for job {job_id}: {str(e)}")
            capture_exception(error)
            raise error

    def trigger_webhook(
        self,
        webhook_path: str,
        payload: Dict[str, Any],
        signature: str,
    ) -> Dict[str, Any]:
        """
        Trigger a job via webhook.

        Note: This method requires proper HMAC signature authentication.
        The signature should be hex(HMAC-SHA256(secret, request_body)).

        Args:
            webhook_path: Webhook path (the unique identifier from webhook URL)
            payload: Dictionary containing:
                - parameters: Dict of parameters to substitute in prompt template
                - config_override: Optional config overrides for this execution
                - metadata: Additional metadata for this trigger
            signature: HMAC signature for the payload

        Returns:
            Dictionary containing trigger response:
                - job_id: Job ID
                - workflow_id: Temporal workflow ID
                - execution_id: Execution UUID
                - status: 'started'
                - message: Success message

        Raises:
            JobError: For API errors
        """
        try:
            endpoint = self._format_endpoint(
                ControlPlaneEndpoints.JOBS_WEBHOOK,
                webhook_path=webhook_path
            )
            # Add signature header for webhook authentication
            headers = {"X-Webhook-Signature": signature}
            response = self._post(endpoint, data=payload, headers=headers)
            return response.json()
        except Exception as e:
            error = JobError(f"Failed to trigger webhook {webhook_path}: {str(e)}")
            capture_exception(error)
            raise error
