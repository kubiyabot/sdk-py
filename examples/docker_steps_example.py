"""
Examples of using docker_build and docker_run step types in Kubiya workflows.

This file demonstrates various use cases for the new Docker step types including:
- Building images from Git repositories
- Multi-platform builds
- Running containers with volumes and environment variables
- Kubernetes deployment scenarios
"""

from kubiya.dsl import Workflow, docker_build_executor, docker_run_executor


def basic_docker_build_workflow():
    """Basic example of building a Docker image."""
    wf = Workflow("build-image")
    wf.description("Build a Docker image from source")

    # Simple build from current directory
    wf.step("build-app").docker_build(
        image="myapp:latest",
        dockerfile="Dockerfile",
        context=".",
        build_args={
            "VERSION": "${VERSION}",
            "BUILD_DATE": "`date -u +%Y-%m-%dT%H:%M:%SZ`"
        }
    )

    return wf


def git_source_build_workflow():
    """Build Docker image from a Git repository."""
    wf = Workflow("build-from-git")
    wf.description("Build Docker image from Git repository")

    # Build from Git repository
    wf.step("clone-and-build").docker_build(
        image="myapp:${GIT_BRANCH}",
        git={
            "url": "https://github.com/myorg/myapp",
            "ref": "${GIT_BRANCH}",
            "token": "${GITHUB_TOKEN}"  # Use secret for authentication
        },
        dockerfile="docker/Dockerfile.production",
        build_args={
            "VERSION": "${GIT_BRANCH}",
            "ENVIRONMENT": "production"
        },
        labels={
            "org.opencontainers.image.source": "https://github.com/myorg/myapp",
            "org.opencontainers.image.revision": "${GIT_COMMIT}"
        },
        push=True,
        registry={
            "url": "registry.example.com",
            "username": "${REGISTRY_USER}",
            "password": "${REGISTRY_PASSWORD}"
        }
    )

    return wf


def multi_platform_build_workflow():
    """Build multi-platform Docker images."""
    wf = Workflow("multi-platform-build")
    wf.description("Build Docker images for multiple architectures")

    # Multi-platform build with buildx
    wf.step("build-multi-arch").docker_build(
        image="myapp:latest",
        platforms=["linux/amd64", "linux/arm64", "linux/arm/v7"],
        build_tool="buildkit",
        build_args={
            "TARGETPLATFORM": "${TARGETPLATFORM}",
            "BUILDPLATFORM": "${BUILDPLATFORM}"
        },
        cache_from=["type=registry,ref=registry.example.com/myapp:cache"],
        cache_to=["type=registry,ref=registry.example.com/myapp:cache,mode=max"],
        push=True
    )

    return wf


def basic_docker_run_workflow():
    """Basic example of running a Docker container."""
    wf = Workflow("run-container")
    wf.description("Run a Docker container with basic configuration")

    # Run a Python script
    wf.step("run-script").docker_run(
        image="python:3.11-slim",
        command=["python", "-c"],
        args=["print('Hello from Docker!')"],
        env={
            "PYTHONUNBUFFERED": "1"
        }
    )

    return wf


def docker_run_with_volumes_workflow():
    """Run Docker container with volume mounts."""
    wf = Workflow("data-processing")
    wf.description("Process data using Docker container with volumes")

    # Process data with volume mounts
    wf.step("process-data").docker_run(
        image="data-processor:latest",
        command=["python", "process.py"],
        volumes=[
            {
                "source": "./input-data",
                "target": "/data/input",
                "type": "bind",
                "read_only": True
            },
            {
                "source": "./output-data",
                "target": "/data/output",
                "type": "bind"
            },
            {
                "source": "config-map",
                "target": "/config",
                "type": "configmap"  # Kubernetes ConfigMap
            }
        ],
        env={
            "INPUT_DIR": "/data/input",
            "OUTPUT_DIR": "/data/output",
            "CONFIG_FILE": "/config/settings.yaml"
        },
        working_dir="/app",
        user="1000:1000",  # Run as non-root user
        memory="4Gi",
        cpu_limit="2"
    )

    return wf


def kubernetes_deployment_workflow():
    """Deploy application to Kubernetes using docker_run."""
    wf = Workflow("k8s-deployment")
    wf.description("Deploy application to Kubernetes cluster")

    # Run in Kubernetes with full configuration
    wf.step("deploy-app").docker_run(
        image="myapp:v2.0.0",
        command=["node", "server.js"],
        env={
            "NODE_ENV": "production",
            "PORT": "8080",
            "DATABASE_URL": "${DATABASE_URL}"
        },
        env_from=[
            {"type": "configmap", "name": "app-config"},
            {"type": "secret", "name": "app-secrets", "prefix": "APP_"}
        ],
        volumes=[
            {
                "source": "app-storage",
                "target": "/data",
                "type": "persistentvolumeclaim"
            }
        ],
        execution_mode="kubernetes",
        namespace="production",
        service_account="app-service-account",
        image_pull_policy="IfNotPresent",
        image_pull_secrets=["registry-secret"],
        restart_policy="OnFailure",
        memory="2Gi",
        cpu_limit="1000m",
        cpu_request="500m",
        node_selector={
            "node-type": "application",
            "environment": "production"
        },
        tolerations=[
            {
                "key": "app-workload",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule"
            }
        ],
        security_context={
            "run_as_user": 1000,
            "run_as_group": 1000,
            "fs_group": 2000,
            "run_as_non_root": True
        },
        labels={
            "app": "myapp",
            "version": "v2.0.0",
            "component": "backend"
        },
        annotations={
            "prometheus.io/scrape": "true",
            "prometheus.io/port": "8080"
        }
    )

    return wf


def ci_cd_pipeline_workflow():
    """Complete CI/CD pipeline using Docker steps."""
    wf = Workflow("ci-cd-pipeline")
    wf.description("Complete CI/CD pipeline with build, test, and deploy stages")
    wf.env(
        GIT_REPO="https://github.com/myorg/myapp",
        REGISTRY="registry.example.com"
    )

    # 1. Build stage
    wf.step("build").docker_build(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        git={
            "url": "${GIT_REPO}",
            "ref": "${GIT_BRANCH}"
        },
        dockerfile="Dockerfile",
        build_args={
            "VERSION": "${GIT_BRANCH}-${BUILD_NUMBER}",
            "BUILD_DATE": "`date -u +%Y-%m-%dT%H:%M:%SZ`"
        },
        target="production",  # Multi-stage build target
        no_cache="${FORCE_BUILD}",  # Allow forcing fresh build
        push=False  # Don't push yet, wait for tests
    )

    # 2. Unit tests
    wf.step("unit-tests").docker_run(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        command=["npm", "test"],
        env={
            "NODE_ENV": "test",
            "CI": "true"
        }
    ).depends("build")

    # 3. Integration tests
    wf.step("integration-tests").docker_run(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        command=["npm", "run", "test:integration"],
        env={
            "NODE_ENV": "test",
            "DATABASE_URL": "postgres://test:test@postgres:5432/testdb"
        },
        volumes=[
            {"source": "./test-data", "target": "/test-data", "type": "bind"}
        ]
    ).depends("build")

    # 4. Security scan
    wf.step("security-scan").docker_run(
        image="aquasec/trivy:latest",
        command=["image", "--severity", "HIGH,CRITICAL"],
        args=["${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}"]
    ).depends("build")

    # 5. Push to registry if all tests pass
    wf.step("push").docker_build(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        push=True,
        tags=[
            "${REGISTRY}/myapp:latest",
            "${REGISTRY}/myapp:${GIT_BRANCH}"
        ],
        registry={
            "url": "${REGISTRY}",
            "username": "${REGISTRY_USER}",
            "password": "${REGISTRY_PASSWORD}"
        }
    ).depends("unit-tests", "integration-tests", "security-scan")

    # 6. Deploy to staging
    wf.step("deploy-staging").docker_run(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        execution_mode="kubernetes",
        namespace="staging",
        env={
            "ENVIRONMENT": "staging"
        }
    ).depends("push")

    # 7. Run smoke tests
    wf.step("smoke-tests").docker_run(
        image="postman/newman:alpine",
        command=["run", "smoke-tests.json"],
        args=["--environment", "staging.json"],
        volumes=[
            {"source": "./postman", "target": "/etc/newman", "type": "bind"}
        ]
    ).depends("deploy-staging")

    # 8. Deploy to production (manual approval can be added here)
    wf.step("deploy-production").docker_run(
        image="${REGISTRY}/myapp:${GIT_BRANCH}-${BUILD_NUMBER}",
        execution_mode="kubernetes",
        namespace="production",
        env={
            "ENVIRONMENT": "production"
        },
        memory="4Gi",
        cpu_limit="2",
        cpu_request="1"
    ).depends("smoke-tests").preconditions("${APPROVE_PRODUCTION} == 'true'")

    return wf


def machine_learning_workflow():
    """Machine learning workflow with GPU support."""
    wf = Workflow("ml-training")
    wf.description("Train machine learning model with GPU acceleration")

    # Build custom ML image
    wf.step("build-ml-image").docker_build(
        image="ml-trainer:latest",
        dockerfile="Dockerfile.ml",
        build_args={
            "CUDA_VERSION": "11.8.0",
            "PYTHON_VERSION": "3.10",
            "TORCH_VERSION": "2.0.1"
        }
    )

    # Train model with GPU
    wf.step("train-model").docker_run(
        image="ml-trainer:latest",
        command=["python", "train.py"],
        args=["--epochs", "100", "--batch-size", "32"],
        env={
            "CUDA_VISIBLE_DEVICES": "0",
            "WANDB_API_KEY": "${WANDB_API_KEY}"
        },
        volumes=[
            {"source": "./datasets", "target": "/data", "type": "bind"},
            {"source": "./models", "target": "/models", "type": "bind"}
        ],
        gpu_limit=1,  # Request 1 GPU
        memory="16Gi",
        cpu_limit="8",
        execution_mode="kubernetes",
        node_selector={
            "accelerator": "nvidia-tesla-v100"
        },
        tolerations=[
            {
                "key": "nvidia.com/gpu",
                "operator": "Exists",
                "effect": "NoSchedule"
            }
        ]
    ).depends("build-ml-image")

    return wf


def development_environment_workflow():
    """Set up development environment using Docker."""
    wf = Workflow("dev-setup")
    wf.description("Set up complete development environment")

    # Build development image with all tools
    wf.step("build-dev-image").docker_build(
        image="dev-env:latest",
        dockerfile="Dockerfile.dev",
        build_args={
            "USER_ID": "`id -u`",
            "GROUP_ID": "`id -g`"
        },
        build_tool="buildkit",
        secrets={
            "npmrc": "${HOME}/.npmrc",
            "ssh": "${HOME}/.ssh/id_rsa"
        }
    )

    # Run development container with live reload
    wf.step("run-dev").docker_run(
        image="dev-env:latest",
        command=["npm", "run", "dev"],
        env={
            "NODE_ENV": "development",
            "DEBUG": "*"
        },
        volumes=[
            {"source": ".", "target": "/workspace", "type": "bind"},
            {"source": "node_modules", "target": "/workspace/node_modules", "type": "volume"}
        ],
        ports=["3000:3000", "9229:9229"],  # App and debug ports
        working_dir="/workspace",
        user="`id -u`:`id -g`",
        network="host",  # Use host network for local development
        execution_mode="local"  # Always run locally
    ).depends("build-dev-image")

    return wf


def using_executor_functions():
    """Example using executor convenience functions."""
    wf = Workflow("executor-example")
    wf.description("Demonstrate executor convenience functions")

    # Use docker_build_executor
    build_step = docker_build_executor(
        "build-api",
        "api:v1.0.0",
        git={"url": "https://github.com/myorg/api", "ref": "v1.0.0"},
        dockerfile="docker/Dockerfile.production",
        build_args={"VERSION": "1.0.0"},
        platforms=["linux/amd64", "linux/arm64"],
        push=True,
        registry={
            "url": "registry.example.com",
            "username": "${REGISTRY_USER}",
            "password": "${REGISTRY_PASSWORD}"
        }
    )
    wf.data["steps"].append(build_step.to_dict())

    # Use docker_run_executor
    run_step = docker_run_executor(
        "run-tests",
        "api:v1.0.0",
        command=["pytest"],
        args=["tests/", "-v", "--cov=api"],
        env={"ENVIRONMENT": "test"},
        volumes=[
            {"source": "./test-fixtures", "target": "/fixtures", "type": "bind"}
        ],
        memory="2Gi",
        cpu_limit="1"
    ).depends("build-api")
    wf.data["steps"].append(run_step.to_dict())

    return wf


if __name__ == "__main__":
    # Print example workflow YAML
    import yaml

    # Select which workflow to demonstrate
    workflow = ci_cd_pipeline_workflow()

    # Convert to YAML and print
    print("# CI/CD Pipeline Workflow Example")
    print(yaml.dump(workflow.to_dict(), default_flow_style=False, sort_keys=False))