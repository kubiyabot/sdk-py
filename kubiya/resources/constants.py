class Endpoints:
    """API endpoint constants"""

    # Workflow endpoints
    WORKFLOW_EXECUTE = "/api/v1/workflow?runner={runner}&operation=execute_workflow"
    WORKFLOW_LIST = "/api/v1/workflow?runner={runner}&operation=list_workflows"
    WORKFLOW_STATUS = "/api/v1/workflow?runner={runner}&operation=get_status"

    # Webhook endpoints
    WEBHOOK_LIST = "/api/v1/event"
    WEBHOOK_GET = "/api/v1/event/{webhook_id}"
    WEBHOOK_CREATE = "/api/v1/event"
    WEBHOOK_UPDATE = "/api/v1/event/{webhook_id}"
    WEBHOOK_DELETE = "/api/v1/event/{webhook_id}"
    WEBHOOK_TEST = "/api/v1/webhook/test"

    # Users endpoints
    USER_LIST = "/api/v2/users"

    # Groups endpoints
    GROUP_LIST = "/api/v1/manage/groups"

    # Tool endpoints
    TOOL_EXECUTE = "/api/v1/tools/exec?runner={runner}"
    TOOL_GENERATE = "/api/v1/http-bridge/v1/generate-tool"
    TOOL_LIST = "/tools"
    TOOL_DESCRIBE = "/tools/{tool_name}"
    TOOL_SEARCH = "/tools/search"

    # Source endpoints - for listing tools from sources
    SOURCES_LIST = "/api/v1/sources"
    SOURCE_GET = "/api/v1/sources/{source_uuid}"
    SOURCE_METADATA = "/api/v1/sources/{source_uuid}/metadata"
    SOURCE_DELETE = "/api/v1/sources/{source_uuid}"
    SOURCE_LOAD = "/api/v1/sources/load"
    SOURCE_ZIP = "/api/v1/sources/zip"
    SOURCE_ZIP_LOAD = "/api/v1/sources/zip/load"
    SOURCE_SYNC = "/api/v1/sources/{source_uuid}/sync"

    # Runner endpoints - for tool execution
    RUNNERS_LIST = "/api/v3/runners"
    RUNNERS_DESCRIBE = "/api/v1/runners/{runner_name}/describe"
    RUNNER_GET = "/api/v3/runners/{runner_name}"
    RUNNER_HELM_CHART = "/api/v3/runners/helmchart/{runner_name}"
    RUNNER_MANIFEST = "/api/v3/runners/{runner_name}"
    RUNNER_HEALTH = "/api/v3/runners/{runner_name}/health"

    # Secrets endpoints
    SECRETS_CREATE = "/api/v1/secrets"
    SECRETS_CREATE_V2 = "/api/v2/secrets"

    SECRETS_LIST = "/api/v1/secrets"
    SECRETS_LIST_V2 = "/api/v2/secrets"

    SECRETS_GET_VALUE = "/api/v1/secret/get_secret_value/{secret_name}"
    SECRETS_GET_VALUE_V2 = "/api/v2/secrets/get_value/{secret_name}"

    SECRETS_UPDATE = "/api/v1/secret/update_secret"
    SECRETS_UPDATE_V2 = "/api/v2/secrets/{secret_name}"

    SECRETS_DELETE = "/api/v1/secret/{secret_name}"
    SECRETS_DELETE_V2 = "/api/v2/secrets/{secret_name}"

    # Project endpoints (tasks and usecases)
    PROJECT_LIST = "/api/v1/usecases"
    PROJECT_GET = "/api/v1/tasks/{project_id}"
    PROJECT_CREATE = "/api/v1/usecases"
    PROJECT_UPDATE = "/api/v1/tasks/{project_id}"
    PROJECT_DELETE = "/api/v1/tasks/{project_id}"
    PROJECT_TEMPLATES_LIST = "/api/v1/usecases"
    PROJECT_TEMPLATE_GET = "/api/v1/usecases/{template_id}"
    PROJECT_PLAN_CREATE = "/api/v1/tasks/plan/{project_id}"
    PROJECT_PLAN_GET = "/api/v1/tasks/plan/{plan_id}"
    PROJECT_PLAN_APPROVE = "/api/v1/tasks/{plan_id}"
    PROJECT_EXECUTION_GET = "/api/v1/tasks/{execution_id}"
    PROJECT_EXECUTION_LOGS = "/api/v1/tasks/logs/{execution_id}"

    # Policy endpoints - for OPA policy management
    POLICY_LIST = "/api/v1/opa/policies"
    POLICY_GET = "/api/v1/opa/policies/{policy_name}"
    POLICY_CREATE = "/api/v1/opa/policies"
    POLICY_UPDATE = "/api/v1/opa/policies/{policy_name}"
    POLICY_DELETE = "/api/v1/opa/policies/{policy_name}"
    POLICY_VALIDATE = "/api/v1/opa/policies/validate"
    POLICY_EVALUATE = "/api/v1/opa/policies/evaluate"

    # Knowledge endpoints
    KNOWLEDGE_QUERY = "/api/query"
    KNOWLEDGE_LIST = "/knowledge"
    KNOWLEDGE_GET = "/knowledge/{knowledge_id}"

    # Integration endpoints
    INTEGRATIONS_LIST_V1 = "/api/v1/integrations"
    INTEGRATIONS_LIST_V2 = "/api/v2/integrations"
    INTEGRATION_GET = "/api/v1/integrations/{integration_name}"
    INTEGRATIONS_GITHUB = "/api/v2/integrations/github_app"
    INTEGRATION_INSTALL = "/api/v1/integration/{integration_name}/install"
    INTEGRATION_CREDENTIALS = "/api/v1/integrations/{vendor}/creds/{id}"

    # Documentation endpoints
    DOCUMENTATION_LIST = "/documentation"
    DOCUMENTATION_GET = "/documentation/{doc_id}"

    # Audit endpoints
    AUDIT_LIST = "/api/v1/auditing/items"
    AUDIT_GET = "/api/v1/auditing/items/{audit_id}"
    AUDIT_STREAM = "/api/v1/auditing/items/stream"

    # Agent endpoints
    AGENTS_LIST = "/api/v1/agents"
    AGENT_GET = "/api/v1/agents/{agent_uuid}"
    AGENT_CREATE = "/api/v1/agents"
    AGENT_UPDATE = "/api/v1/agents/{agent_uuid}"
    AGENT_DELETE = "/api/v1/agents/{agent_uuid}"

    # Stacks endpoints
    STACKS_PLAN = "api/v1/tasks/inline/plan"
    STACKS_APPLY = "/api/v1/tasks/inline"
    STACKS_STREAM = "/api/v1/tasks/stream/logs/{stack_id}"


class ControlPlaneEndpoints:
    """Control Plane API endpoint constants"""

    # Health endpoints
    HEALTH = "/api/health"
    READY = "/api/ready"
    HEALTH_DETAILED = "/api/health/detailed"

    # Model endpoints
    MODELS_LIST = "/api/v1/models"
    MODELS_GET = "/api/v1/models/{model_id}"
    MODELS_CREATE = "/api/v1/models"
    MODELS_UPDATE = "/api/v1/models/{model_id}"
    MODELS_DELETE = "/api/v1/models/{model_id}"
    MODELS_DEFAULT = "/api/v1/models/default"
    MODELS_PROVIDERS = "/api/v1/models/providers"

    # Runtime endpoints
    RUNTIMES_LIST = "/api/v1/runtimes"
    RUNTIME_REQUIREMENTS = "/api/v1/runtimes/{runtime_id}/requirements"
    RUNTIME_VALIDATE = "/api/v1/runtimes/validate"

    # Context endpoints
    CONTEXT_GET = "/api/v1/context/{entity_type}/{entity_id}"
    CONTEXT_UPDATE = "/api/v1/context/{entity_type}/{entity_id}"
    CONTEXT_DELETE = "/api/v1/context/{entity_type}/{entity_id}"
    CONTEXT_RESOLVE = "/api/v1/context/resolve/{entity_type}/{entity_id}"

    # Skills endpoints
    SKILLS_LIST = "/api/v1/skills"
    SKILLS_GET = "/api/v1/skills/{skill_id}"
    SKILLS_CREATE = "/api/v1/skills"
    SKILLS_UPDATE = "/api/v1/skills/{skill_id}"
    SKILLS_DELETE = "/api/v1/skills/{skill_id}"
    SKILLS_ASSOCIATE = "/api/v1/skills/associate"
    SKILLS_VALIDATE = "/api/v1/skills/validate"

    # Policies endpoints
    POLICIES_LIST = "/api/v1/policies"
    POLICIES_GET = "/api/v1/policies/{policy_id}"
    POLICIES_CREATE = "/api/v1/policies"
    POLICIES_UPDATE = "/api/v1/policies/{policy_id}"
    POLICIES_DELETE = "/api/v1/policies/{policy_id}"
    POLICIES_EVALUATE = "/api/v1/policies/evaluate"
    POLICIES_AUTHORIZE = "/api/v1/policies/authorize"

    # Task planning endpoints
    TASK_PLANNING_PLAN = "/api/v1/planning/plan"
    TASK_PLANNING_PLAN_STREAM = "/api/v1/planning/plan/stream"

    # Agents endpoints
    AGENTS_LIST = "/api/v1/agents"
    AGENTS_GET = "/api/v1/agents/{agent_id}"
    AGENTS_CREATE = "/api/v1/agents"
    AGENTS_UPDATE = "/api/v1/agents/{agent_id}"
    AGENTS_DELETE = "/api/v1/agents/{agent_id}"
    AGENTS_EXECUTE = "/api/v1/agents/{agent_id}/execute"

    # Workers endpoints
    WORKERS_LIST = "/api/v1/workers"
    WORKERS_GET = "/api/v1/workers/{runner_name}"
    WORKERS_REGISTER = "/api/v1/workers/register"
    WORKERS_HEARTBEAT = "/api/v1/workers/heartbeat"
    WORKERS_HEARTBEAT_SIMPLE = "/api/v1/workers/{worker_id}/heartbeat"
    WORKERS_START = "/api/v1/workers/{worker_id}/start"
    WORKERS_DISCONNECT = "/api/v1/workers/{worker_id}/disconnect"

    # Secrets endpoints
    SECRETS_LIST = "/api/v1/secrets"
    SECRETS_VALUE = "/api/v1/secrets/value/{name}"

    # Integrations endpoints
    INTEGRATIONS_LIST = "/api/v1/integrations"
    INTEGRATIONS_GET = "/api/v1/integrations/{integration_id}"
    INTEGRATION_CREDENTIALS = "/api/v1/integrations/{vendor}/creds/{id}"

    # Context Graph endpoints
    GRAPH_HEALTH = "/api/v1/context-graph/health"
    GRAPH_NODES_LIST = "/api/v1/context-graph/api/v1/graph/nodes"
    GRAPH_NODES_GET = "/api/v1/context-graph/api/v1/graph/nodes/{node_id}"
    GRAPH_NODES_SEARCH = "/api/v1/context-graph/api/v1/graph/nodes/search"
    GRAPH_NODES_SEARCH_TEXT = "/api/v1/context-graph/api/v1/graph/nodes/search/text"
    GRAPH_RELATIONSHIPS = "/api/v1/context-graph/api/v1/graph/nodes/{node_id}/relationships"
    GRAPH_SUBGRAPH = "/api/v1/context-graph/api/v1/graph/subgraph"
    GRAPH_LABELS = "/api/v1/context-graph/api/v1/graph/labels"
    GRAPH_RELATIONSHIP_TYPES = "/api/v1/context-graph/api/v1/graph/relationship-types"
    GRAPH_STATS = "/api/v1/context-graph/api/v1/graph/stats"
    GRAPH_QUERY = "/api/v1/context-graph/api/v1/graph/query"
    GRAPH_INTEGRATIONS = "/api/v1/context-graph/api/v1/graph/integrations"