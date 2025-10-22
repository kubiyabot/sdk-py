"""
Kubiya Workflow DSL - Simple, intuitive workflow creation.

A comprehensive DSL that supports all Kubiya workflow features with clean,
chainable API and proper separation of concerns.
"""

from kubiya.dsl.workflow import Workflow, workflow, chain, graph
from kubiya.dsl.step import Step, step, parallel_step, conditional_step
from kubiya.dsl.executors import (
    python_executor,
    shell_executor,
    docker_executor,
    http_executor,
    ssh_executor,
    inline_agent_executor,
)
from kubiya.dsl.data import Output, Param, EnvVar, Secret
from kubiya.dsl.control_flow import when, retry_policy, repeat_policy, continue_on, precondition
from kubiya.dsl.lifecycle import HandlerOn, MailOn, Notifications
from kubiya.dsl.queue import Queue, QueueConfig
from kubiya.dsl.scheduling import Schedule
from kubiya.dsl.examples import examples
from kubiya.dsl.executors import tool_executor, kubiya_executor, jq_executor

__all__ = [
    # Workflow builders
    "Workflow",
    "workflow",
    "chain",
    "graph",
    # Step builders
    "Step",
    "step",
    "parallel_step",
    "conditional_step",
    # Executors
    "python_executor",
    "shell_executor",
    "docker_executor",
    "http_executor",
    "ssh_executor",
    "inline_agent_executor",
    "tool_executor",
    "kubiya_executor",
    "jq_executor",
    # Data handling
    "Output",
    "Param",
    "EnvVar",
    "Secret",
    # Control flow
    "when",
    "retry_policy",
    "repeat_policy",
    "continue_on",
    "precondition",
    # Lifecycle
    "HandlerOn",
    "MailOn",
    "Notifications",
    # Queue management
    "Queue",
    "QueueConfig",
    # Scheduling
    "Schedule",
    # Examples
    "examples",
]
