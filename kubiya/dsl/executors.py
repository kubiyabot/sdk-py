"""
Executor convenience functions for easy step creation.

These functions provide shortcuts for creating steps with specific executor types.
"""

from typing import Dict, Any, List, Optional
from kubiya.dsl.step import Step


def python_executor(name: str, script: str, **kwargs) -> Step:
    """
    Create a Python script step.

    Example:
        python_executor("process", '''
            import json
            data = json.loads(input())
            print(json.dumps({"result": len(data)}))
        ''')
    """
    return Step(name).python(script)


def shell_executor(name: str, command: str, shell: str = "sh", **kwargs) -> Step:
    """
    Create a shell command step.

    Example:
        shell_executor("backup", "tar -czf backup.tar.gz /data")
    """
    step = Step(name, command)
    if shell != "sh":
        step.shell_type(shell)
    return step


def docker_executor(
    name: str, image: str, command: Optional[str] = None, content: Optional[str] = None, **kwargs
) -> Step:
    """
    Create a Docker container step.

    Example:
        docker_executor("build", "node:18", "npm run build")
    """
    return Step(name).docker(image, command, content)


def http_executor(
    name: str,
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Any] = None,
    **kwargs,
) -> Step:
    """
    Create an HTTP request step.

    Example:
        http_executor("webhook", "https://api.example.com/webhook",
                     method="POST",
                     headers={"Content-Type": "application/json"},
                     body={"status": "started"})
    """
    return Step(name).http(url, method, headers, body)


def ssh_executor(
    name: str,
    host: str,
    user: str,
    command: str,
    port: int = 22,
    key_file: Optional[str] = None,
    **kwargs,
) -> Step:
    """
    Create an SSH remote execution step.

    Example:
        ssh_executor("deploy", "server.example.com", "deploy",
                    "./deploy.sh", key_file="/home/user/.ssh/id_rsa")
    """
    return Step(name).ssh(host, user, command, port, key_file)


def inline_agent_executor(
    name: str,
    message: str,
    agent_name: str,
    ai_instructions: str,
    runners: List[str] = ["core-testing-2"],
    llm_model: str = "gpt-4o-mini",
    tools: Optional[List[Dict[str, Any]]] = None,
    **kwargs,
) -> Step:
    """
    Create an inline AI agent step.

    Example:
        inline_agent_executor(
            "analyze-logs",
            "Analyze these logs and find errors: {{logs}}",
            agent_name="log-analyzer",
            ai_instructions="You are a log analysis expert. Find patterns and errors.",
            llm_model="gpt-4o"
        )
    """
    return Step(name).inline_agent(
        message=message,
        agent_name=agent_name,
        ai_instructions=ai_instructions,
        runners=runners,
        llm_model=llm_model,
        tools=tools,
        **kwargs,
    )


def tool_executor(
    name: str, tool_name: str = None, tool_def: Dict[str, Any] = None, **tool_args
) -> Step:
    """
    Create a tool executor step.

    Example with pre-registered tool:
        tool_executor("get-pods", tool_name="kubectl", command="get pods -n default")

    Example with inline tool definition:
        tool_executor("notify",
                     tool_def={
                         "name": "slack-notifier",
                         "type": "docker",
                         "image": "curlimages/curl:latest",
                         "content": "#!/bin/sh\\ncurl -X POST...",
                         "args": [{"name": "channel", "type": "string"}]
                     },
                     channel="#alerts",
                     message="Error detected!")
    """
    if tool_def:
        # Inline tool definition
        step = Step(name).tool_def(
            name=tool_def["name"],
            type=tool_def["type"],
            image=tool_def["image"],
            content=tool_def["content"],
            args=tool_def["args"],
            description=tool_def.get("description"),
            with_files=tool_def.get("with_files"),
        )
        if tool_args:
            step.args(**tool_args)
        return step
    elif tool_name:
        # Pre-registered tool
        return Step(name).tool(tool_name, **tool_args)
    else:
        raise ValueError("Either tool_name or tool_def must be provided")


def kubiya_executor(name: str, url: str, method: str = "GET", **config) -> Step:
    """
    Create a Kubiya API executor step.

    Example:
        kubiya_executor("get-secret", "api/v1/secret/get_secret_value/MY_SECRET")
    """
    return Step(name).kubiya(url, method, **config)


def jq_executor(name: str, query: str, **kwargs) -> Step:
    """
    Create a jq JSON processing step.

    Example:
        jq_executor("extract-ids", '.data[] | select(.active == true) | .id')
    """
    return Step(name).jq(query)


def docker_build_executor(
    name: str,
    image: str,
    push: bool = False,
    no_cache: bool = False,
    git: Optional[Dict[str, Any]] = None,
    dockerfile: Optional[str] = None,
    context: Optional[str] = None,
    tags: Optional[List[str]] = None,
    platforms: Optional[List[str]] = None,
    build_args: Optional[Dict[str, str]] = None,
    labels: Optional[Dict[str, str]] = None,
    target: Optional[str] = None,
    registry: Optional[Dict[str, str]] = None,
    execution_mode: Optional[str] = None,
    **kwargs,
) -> Step:
    """
    Create a Docker build step.

    Args:
        name: Step name
        image: Image name to build (required)
        git: Git repository configuration (url, ref, token, etc.)
        dockerfile: Path to Dockerfile (default: Dockerfile)
        context: Build context path (default: .)
        tags: Additional tags for the image
        platforms: Target platforms for multi-platform builds
        push: Whether to push to registry after build
        no_cache: Build without using cache
        build_args: Build-time arguments
        labels: Image labels/metadata
        target: Multi-stage build target
        registry: Registry configuration (url, username, password)
        execution_mode: auto/local/kubernetes/openshift (default: auto)

    Example:
        docker_build_executor(
            "build-api",
            "myapp/api:latest",
            git={"url": "https://github.com/myapp/api", "ref": "v1.0.0"},
            dockerfile="Dockerfile.prod",
            build_args={"VERSION": "1.0.0", "ENV": "production"},
            platforms=["linux/amd64", "linux/arm64"],
            push=True,
            registry={"url": "registry.example.com", "username": "$REGISTRY_USER", "password": "$REGISTRY_PASS"}
        )
    """
    config = {}
    if git is not None:
        config["git"] = git
    if dockerfile is not None:
        config["dockerfile"] = dockerfile
    if context is not None:
        config["context"] = context
    if tags is not None:
        config["tags"] = tags
    if platforms is not None:
        config["platforms"] = platforms
    if push:
        config["push"] = push
    if no_cache:
        config["no_cache"] = no_cache
    if build_args is not None:
        config["build_args"] = build_args
    if labels is not None:
        config["labels"] = labels
    if target is not None:
        config["target"] = target
    if registry is not None:
        config["registry"] = registry
    if execution_mode is not None:
        config["execution_mode"] = execution_mode

    # Add any additional kwargs
    config.update(kwargs)

    return Step(name).docker_build(image, **config)


def docker_run_executor(
    name: str,
    image: str,
    command: Optional[List[str]] = None,
    args: Optional[List[str]] = None,
    env: Optional[Dict[str, str]] = None,
    env_from: Optional[List[Dict[str, Any]]] = None,
    volumes: Optional[List[Dict[str, Any]]] = None,
    working_dir: Optional[str] = None,
    user: Optional[str] = None,
    memory: Optional[str] = None,
    cpu_limit: Optional[str] = None,
    cpu_request: Optional[str] = None,
    gpu_limit: Optional[int] = None,
    execution_mode: Optional[str] = None,
    namespace: Optional[str] = None,
    service_account: Optional[str] = None,
    security_context: Optional[Dict[str, Any]] = None,
    node_selector: Optional[Dict[str, str]] = None,
    tolerations: Optional[List[Dict[str, Any]]] = None,
    **kwargs,
) -> Step:
    """
    Create an enhanced Docker run step with Kubernetes support.

    Args:
        name: Step name
        image: Container image to run (required)
        command: Command to override entrypoint
        args: Arguments for the container
        env: Environment variables
        env_from: Environment from configmaps/secrets
        volumes: Volume mounts
        working_dir: Working directory in container
        user: User to run as (uid or username)
        memory: Memory limit (e.g., "2Gi")
        cpu_limit: CPU limit (e.g., "2")
        cpu_request: CPU request (Kubernetes)
        gpu_limit: Number of GPUs
        execution_mode: auto/local/kubernetes/openshift
        namespace: Kubernetes namespace
        service_account: Kubernetes service account
        security_context: Security settings
        node_selector: Node selection constraints
        tolerations: Pod tolerations

    Example:
        docker_run_executor(
            "run-tests",
            "python:3.11",
            command=["python", "-m", "pytest"],
            args=["tests/", "-v", "--cov"],
            env={"ENV": "test", "DB_HOST": "localhost"},
            volumes=[
                {"source": "./app", "target": "/app", "type": "bind"},
                {"source": "test-data", "target": "/data", "type": "configmap"}
            ],
            memory="4Gi",
            cpu_limit="2",
            execution_mode="kubernetes"
        )
    """
    config = {}

    if command is not None:
        config["command"] = command
    if args is not None:
        config["args"] = args
    if env is not None:
        config["env"] = env
    if env_from is not None:
        config["env_from"] = env_from
    if volumes is not None:
        config["volumes"] = volumes
    if working_dir is not None:
        config["working_dir"] = working_dir
    if user is not None:
        config["user"] = user
    if memory is not None:
        config["memory"] = memory
    if cpu_limit is not None:
        config["cpu_limit"] = cpu_limit
    if cpu_request is not None:
        config["cpu_request"] = cpu_request
    if gpu_limit is not None:
        config["gpu_limit"] = gpu_limit
    if execution_mode is not None:
        config["execution_mode"] = execution_mode
    if namespace is not None:
        config["namespace"] = namespace
    if service_account is not None:
        config["service_account"] = service_account
    if security_context is not None:
        config["security_context"] = security_context
    if node_selector is not None:
        config["node_selector"] = node_selector
    if tolerations is not None:
        config["tolerations"] = tolerations

    # Add any additional kwargs
    config.update(kwargs)

    return Step(name).docker_run(image, **config)
