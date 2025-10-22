import os
import json
import logging
from typing import Any, Dict
from urllib.parse import urlparse

import sentry_sdk
from fastapi import APIRouter, HTTPException, status
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from kubiya.server.core import run_tool, load_workflows_and_tools, run_workflow_with_progress
from kubiya.core import KubiyaJSONEncoder
from kubiya.core.models.server import (
    RunRequest,
    DescribeRequest,
    DiscoverRequest,
    VisualizeRequest,
)

try:
    from setuptools.errors import SetupError as DistutilsArgError # For python >= 3.12
except ImportError:
    try:
        from distutils.errors import DistutilsArgError  # for python < 3.12
    except ImportError:
        class DistutilsArgError(Exception):  # Fallback if neither works
            pass

# Set up logging
logger = logging.getLogger("kubiya")
logging.basicConfig(level=logging.INFO)

# Set up Sentry if DSN is provided
sentry_dsn = os.environ.get("SENTRY_DSN")

def filter_transactions(event, _):
    url_string = event["request"]["url"]
    parsed_url = urlparse(url_string)

    if parsed_url.path in ["/metrics", "/healthz"]:
        return None

    return event


if sentry_dsn:
    logger.info("[BOOT] Setting up Sentry")
    sentry_sdk.init(
        dsn=sentry_dsn,  # Use your existing DSN
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        before_send_transaction=filter_transactions,
        integrations=[
            FastApiIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
    )
    logger.info("Sentry monitoring initialized")
else:
    logger.warning("SENTRY_DSN not found in environment variables. Sentry monitoring is disabled.")

router = APIRouter()

@router.get(
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def get_health():
    # Increment health request counter for metrics
    if not hasattr(get_health, '_health_requests'):
        get_health._health_requests = 0
    get_health._health_requests += 1
    
    # Share counter with metrics endpoint
    if not hasattr(get_metrics, '_health_requests'):
        get_metrics._health_requests = 0
    get_metrics._health_requests += 1
    
    return {"status": "ok"}


@router.get(
    "/metrics",
    summary="Prometheus metrics endpoint",
    response_description="Return Prometheus metrics in text format",
    status_code=status.HTTP_200_OK,
    response_class=None,  # Use plain text response
)
def get_metrics():
    import time
    import os
    from fastapi import Response
    
    # Try to import psutil, set fallback values if not available
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        psutil_available = True
    except ImportError:
        # Fallback if psutil is not available
        cpu_percent = 0
        memory = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        disk = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        process_memory = type('obj', (object,), {'rss': 0, 'vms': 0})()
        psutil_available = False
    except Exception:
        # Fallback if psutil import succeeds but metrics collection fails
        cpu_percent = 0
        memory = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        disk = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 0})()
        process_memory = type('obj', (object,), {'rss': 0, 'vms': 0})()
        psutil_available = False
    
    # Build Prometheus-compatible metrics
    metrics_text = f"""# HELP kubiya_info Information about the Kubiya SDK
# TYPE kubiya_info gauge
kubiya_info{{version="1.18.1",python_version="{os.sys.version.split()[0]}",psutil_available="{str(psutil_available).lower()}"}} 1

# HELP kubiya_health_status Health status of the Kubiya SDK
# TYPE kubiya_health_status gauge
kubiya_health_status 1

# HELP kubiya_system_metrics_available Whether system metrics collection is available
# TYPE kubiya_system_metrics_available gauge
kubiya_system_metrics_available {int(psutil_available)}

# HELP kubiya_uptime_seconds Uptime of the Kubiya SDK server in seconds
# TYPE kubiya_uptime_seconds counter
kubiya_uptime_seconds {time.time()}

# HELP kubiya_cpu_usage_percent CPU usage percentage
# TYPE kubiya_cpu_usage_percent gauge
kubiya_cpu_usage_percent {cpu_percent}

# HELP kubiya_memory_usage_bytes Memory usage in bytes
# TYPE kubiya_memory_usage_bytes gauge
kubiya_memory_usage_bytes {getattr(memory, 'used', 0)}

# HELP kubiya_memory_usage_percent Memory usage percentage
# TYPE kubiya_memory_usage_percent gauge
kubiya_memory_usage_percent {getattr(memory, 'percent', 0)}

# HELP kubiya_disk_usage_bytes Disk usage in bytes
# TYPE kubiya_disk_usage_bytes gauge
kubiya_disk_usage_bytes {getattr(disk, 'used', 0)}

# HELP kubiya_disk_usage_percent Disk usage percentage
# TYPE kubiya_disk_usage_percent gauge
kubiya_disk_usage_percent {getattr(disk, 'percent', 0)}

# HELP kubiya_process_memory_rss Process RSS memory in bytes
# TYPE kubiya_process_memory_rss gauge
kubiya_process_memory_rss {getattr(process_memory, 'rss', 0)}

# HELP kubiya_process_memory_vms Process VMS memory in bytes
# TYPE kubiya_process_memory_vms gauge
kubiya_process_memory_vms {getattr(process_memory, 'vms', 0)}

# HELP kubiya_requests_total Total number of requests processed by endpoint
# TYPE kubiya_requests_total counter
kubiya_requests_total{{endpoint="/health",method="GET",status="200"}} {getattr(get_metrics, '_health_requests', 0)}
kubiya_requests_total{{endpoint="/metrics",method="GET",status="200"}} {getattr(get_metrics, '_metrics_requests', 0)}
kubiya_requests_total{{endpoint="/discover",method="POST",status="200"}} {getattr(get_metrics, '_discover_requests', 0)}
kubiya_requests_total{{endpoint="/run",method="POST",status="200"}} {getattr(get_metrics, '_run_requests', 0)}
kubiya_requests_total{{endpoint="/describe",method="POST",status="200"}} {getattr(get_metrics, '_describe_requests', 0)}
kubiya_requests_total{{endpoint="/visualize",method="POST",status="200"}} {getattr(get_metrics, '_visualize_requests', 0)}
"""
    
    # Increment metrics request counter
    if not hasattr(get_metrics, '_metrics_requests'):
        get_metrics._metrics_requests = 0
    get_metrics._metrics_requests += 1
    
    return Response(content=metrics_text, media_type="text/plain")


@router.post(
    "/discover",
    response_model=Dict[str, Any],
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    },
)
async def discover_endpoint(request: DiscoverRequest):
    # Increment discover request counter for metrics
    if not hasattr(get_metrics, '_discover_requests'):
        get_metrics._discover_requests = 0
    get_metrics._discover_requests += 1
    
    if not request.source:
        logger.error("Invalid request: source is required")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Source is required")

    try:
        logger.info(f"Discovering workflows and tools from source: {request.source}")
        results = load_workflows_and_tools(request.source, request.dynamic_config)

        if not results:
            logger.warning(f"No workflows or tools found in source: {request.source}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No workflows or tools found",
            )

        return json.loads(json.dumps(results, cls=KubiyaJSONEncoder))
    except DistutilsArgError as e:
        logger.warning(f"Invalid setup command in the source '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid setup command: {str(e)}",
        )
    except SystemExit as e:
        logger.warning(f"System exit encountered while processing '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"System exit encountered: {str(e)}",
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON encoding error: {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error encoding response: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error during discovery: {str(e)}", exc_info=True)
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/run",
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    },
)
async def run_endpoint(request: RunRequest):
    # Increment run request counter for metrics
    if not hasattr(get_metrics, '_run_requests'):
        get_metrics._run_requests = 0
    get_metrics._run_requests += 1
    
    try:
        logger.info(f"Running workflow or tool '{request.name}' from source: {request.source}")
        results = load_workflows_and_tools(request.source, {})
        workflow = next((w for w in results["workflows"] if w["name"] == request.name), None)
        tool = next((t for t in results["tools"] if t.name == request.name), None)

        if workflow:
            logger.debug(f"Running workflow: {request.name}")
            result = run_workflow_with_progress(workflow["instance"], request.inputs)
            return list(result)
        elif tool:
            logger.debug(f"Running tool: {request.name}")
            result = await run_tool(tool, request.inputs)
            return result
        else:
            logger.warning(f"Workflow or tool '{request.name}' not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow or tool '{request.name}' not found",
            )
    except DistutilsArgError as e:
        logger.warning(f"Invalid setup command in the source '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid setup command: {str(e)}",
        )
    except SystemExit as e:
        logger.warning(f"System exit encountered while processing '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"System exit encountered: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error during run: {str(e)}", exc_info=True)
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/describe",
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    },
)
async def describe_endpoint(request: DescribeRequest):
    # Increment describe request counter for metrics
    if not hasattr(get_metrics, '_describe_requests'):
        get_metrics._describe_requests = 0
    get_metrics._describe_requests += 1
    
    try:
        logger.info(f"Describing workflow or tool '{request.name}' from source: {request.source}")
        results = load_workflows_and_tools(request.source, {})
        workflow = next((w for w in results["workflows"] if w["name"] == request.name), None)
        tool = next((t for t in results["tools"] if t.name == request.name), None)

        if workflow:
            logger.debug(f"Describing workflow: {request.name}")
            description = {
                "type": "workflow",
                "name": workflow["name"],
                "description": workflow["instance"].description,
                "steps": [
                    {
                        "name": name,
                        "description": step.description,
                        "icon": step.icon,
                        "label": step.label,
                        "next_steps": step.next_steps,
                        "conditions": step.conditions,
                    }
                    for name, step in workflow["instance"].steps.items()
                ],
                "entry_point": workflow["instance"].entry_point,
            }
        elif tool:
            logger.debug(f"Describing tool: {request.name}")
            description = {
                "type": "tool",
                "name": tool.name,
                "description": tool.description,
                "args": [arg.dict() for arg in tool.args],
                "env": tool.env,
            }
        else:
            logger.warning(f"Workflow or tool '{request.name}' not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow or tool '{request.name}' not found",
            )

        return json.loads(json.dumps(description, cls=KubiyaJSONEncoder))
    except DistutilsArgError as e:
        logger.warning(f"Invalid setup command in the source '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid setup command: {str(e)}",
        )
    except SystemExit as e:
        logger.warning(f"System exit encountered while processing '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"System exit encountered: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error during describe: {str(e)}", exc_info=True)
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.post(
    "/visualize",
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        422: {"description": "Unprocessable Entity"},
        500: {"description": "Internal Server Error"},
    },
)
async def visualize_endpoint(request: VisualizeRequest):
    # Increment visualize request counter for metrics
    if not hasattr(get_metrics, '_visualize_requests'):
        get_metrics._visualize_requests = 0
    get_metrics._visualize_requests += 1
    
    try:
        logger.info(f"Visualizing workflow '{request.workflow}' from source: {request.source}")
        results = load_workflows_and_tools(request.source, {})
        workflow = next((w for w in results["workflows"] if w["name"] == request.workflow), None)

        if workflow:
            logger.debug(f"Generating Mermaid diagram for workflow: {request.workflow}")
            mermaid_diagram = workflow["instance"].to_mermaid()
            return {"name": request.workflow, "diagram": mermaid_diagram}
        else:
            logger.warning(f"Workflow '{request.workflow}' not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow '{request.workflow}' not found",
            )
    except DistutilsArgError as e:
        logger.warning(f"Invalid setup command in the source '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid setup command: {str(e)}",
        )
    except SystemExit as e:
        logger.warning(f"System exit encountered while processing '{request.source}': {str(e)}")
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"System exit encountered: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error during visualization: {str(e)}", exc_info=True)
        if sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )

