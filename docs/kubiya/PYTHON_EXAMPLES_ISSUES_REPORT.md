# Python Examples Issues Report - Kubiya Documentation

**Report Date:** 2025-10-04  
**Analyzed Files:** 16+ documentation files in `docs/kubiya/`

This report identifies Python code examples in the Kubiya documentation that contain errors, incorrect API usage, or inconsistencies with the actual SDK implementation.

---

## Summary

**Total Issues Found:** 18  
**Severity Levels:**
- 🔴 **Critical** (breaks code execution): 6
- 🟡 **Warning** (incorrect but may work): 8  
- 🟢 **Minor** (style/consistency issues): 4

---

## Critical Issues 🔴

### 1. Missing JSON Import in Streaming Example
**File:** `tutorials/ai-powered-automation.mdx`  
**Lines:** 186-197  
**Issue:** `json.loads()` is used without importing the `json` module at the top of the code block.

**Current Code:**
```python
async for event in adk.compose(
    task=task,
    mode="act",
    stream=True
):
    # Handle streaming events
    if isinstance(event, str) and event.startswith("data: "):
        data = json.loads(event[6:])  # ❌ json not imported
```

**Fix:**
```python
import json  # Add at the top

async for event in adk.compose(...):
    if isinstance(event, str) and event.startswith("data: "):
        data = json.loads(event[6:])
```

---

### 2. Incorrect Class Name: `Kubiya` vs `KubiyaClient`
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 85-92, 103-106, 298-304  
**Issue:** Documentation uses `Kubiya` class which doesn't exist. The actual class is `KubiyaClient`.

**Current Code:**

```python
from kubiya import Kubiya  # ❌ No such class

client = Kubiya(
    api_key="your-api-key-here",
    organization="your-organization"
)
```

**Fix:**

```python
from kubiya import KubiyaClient  # ✅ Correct class name

client = KubiyaClient(
    api_key="your-api-key-here",
    organization="your-organization"
)
```

**Affected Locations:**
- Line 85: `from kubiya import Kubiya`
- Line 106: `client = Kubiya()`
- Line 299: `client = AsyncKubiya()`

---

### 3. Non-Existent `AsyncKubiya` Class
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 298-304  
**Issue:** `AsyncKubiya` class doesn't exist in the SDK.

**Current Code:**

```python
from kubiya import AsyncKubiya  # ❌ No such class


async def parallel_deployments():
    client = AsyncKubiya()
```

**Fix:**

```python
from kubiya import KubiyaClient


async def parallel_deployments():
    client = KubiyaClient()
    # Use the same client with async methods
```

---

### 4. Incorrect Method: `.compose()` on `Kubiya` Client
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 109-124, 352-356  
**Issue:** The `KubiyaClient` doesn't have a `.compose()` method directly on the client.

**Current Code:**
```python
client = Kubiya()

result = client.compose(  # ❌ No compose method on client
    goal="Check the health of all services in production",
    mode="act",
    stream=False
)
```

**Expected API:** Based on the SDK structure, this should likely use a provider or different method.

---

### 5. Standard Library in Requirements
**File:** `tools/function-tools.mdx`  
**Line:** 601  
**Issue:** `concurrent.futures` is included in requirements, but it's a Python standard library module.

**Current Code:**
```python
@function_tool(
    description="Process multiple files in batch",
    requirements=["concurrent.futures"]  # ❌ Standard library
)
```

**Fix:**
```python
@function_tool(
    description="Process multiple files in batch",
    requirements=[]  # Remove - no external dependencies needed
)
def batch_process(...):
    from concurrent.futures import ThreadPoolExecutor
```

---

### 6. Missing Imports in MCP Examples
**File:** `mcpserver/overview.mdx`  
**Lines:** 185-220  
**Issue:** Python code block is missing critical imports at the beginning.

**Current Code:**
```python
# Code starts with:
async def use_kubiya_tools():
    server_params = StdioServerParameters(  # ❌ Not imported
```

**Fix:**
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import StdioServerTransport

async def use_kubiya_tools():
    server_params = StdioServerParameters(...)
```

---

## Warning Issues 🟡

### 7. Inconsistent Workflow API Usage
**File:** `sdk/quickstart.mdx`  
**Lines:** 159-224  
**Issue:** Uses `Workflow`, `Step`, `Parallel` classes that aren't documented as top-level exports.

**Current Code:**

```python
from kubiya import Workflow, Step, Parallel
from kubiya.tools import KubectlTool, SlackTool, DatadogTool


def create_deployment_workflow():
    workflow = Workflow(
        name="safe-microservice-deployment",
        description="Deploy microservice with health checks and rollback"
    )
```

**Issue:** The actual SDK exports `workflow` and `step` as functions, not classes. This may be an older API or incorrect documentation.

---

### 8. Undefined `configure` Function
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 72-81  
**Issue:** Uses `configure()` function that's not in the SDK exports.

**Current Code:**

```python
from kubiya import configure  # ❌ Not in __init__.py

configure(
    api_key="your-api-key-here",
    organization="your-organization",
    base_url="https://api.kubiya.ai"
)
```

---

### 9. Incorrect Import Path for Exceptions
**File:** `sdk/client/overview.mdx`  
**Lines:** 81, 110, 152, etc.  
**Issue:** Uses `kubiya.kubiya_services.exceptions` which doesn't match the actual structure.

**Current Code:**

```python
from kubiya.kubiya_services.exceptions import AgentError  # ❌
```

**Expected:**

```python
from kubiya.core.exceptions import AgentError  # ✅
# OR
from kubiya import AgentError  # If exported at top level
```

---

### 10. Missing uuid Import
**File:** `tutorials/ai-powered-automation.mdx`  
**Line:** 412  
**Issue:** Uses `uuid.uuid4()` without importing uuid module.

**Current Code:**
```python
async def refine_workflow():
    adk = get_provider("adk")
    session_id = str(uuid.uuid4())  # ❌ uuid not imported
```

**Fix:**
```python
import uuid

async def refine_workflow():
    adk = get_provider("adk")
    session_id = str(uuid.uuid4())
```

---

### 11. Undefined `handle_event` Function
**File:** `tutorials/ai-powered-automation.mdx`  
**Lines:** 298, 179  
**Issue:** Calls `handle_event()` function that is never defined.

**Current Code:**
```python
async for event in adk.compose(...):
    handle_event(event)  # ❌ Function not defined
```

---

### 12. Missing time Import
**File:** `tutorials/ai-powered-automation.mdx`  
**Line:** 513  
**Issue:** Uses `time.time()` without importing time module.

**Current Code:**
```python
start = time.time()  # ❌ time not imported
```

---

### 13. WorkflowError vs WorkflowExecutionError
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 367-407  
**Issue:** Uses `WorkflowError` which may not be the correct exception class.

**Current Code:**

```python
from kubiya import Kubiya, WorkflowError  # May be WorkflowExecutionError
```

**Note:** The SDK exports `WorkflowExecutionError`, not `WorkflowError`.

---

### 14. Incorrect Tool Class Instantiation
**File:** `quickstart/sdk-quickstart.mdx`  
**Lines:** 414-475  
**Issue:** Uses `Tool` class incorrectly - inheriting from it with class attributes instead of instantiation.

**Current Code:**
```python
class CustomMonitoringTool(Tool):
    name = "company-monitor"
    description = "Monitor internal services"
    parameters = [...]
    
    def execute(self, context):
        ...
```

**Issue:** This appears to be a class-based approach that may not match the actual Tool API.

---

## Minor Issues 🟢

### 15. Missing datetime Import
**File:** `sdk/workflow-dsl/overview.mdx`  
**Line:** 179, 448  
**Issue:** Uses `datetime.now()` without importing datetime.

**Current Code:**
```python
"timestamp": datetime.now().isoformat()  # ❌ datetime not imported
```

---

### 16. Inconsistent Parameter Naming
**File:** `sdk/client/overview.mdx`  
**Lines:** Multiple locations  
**Issue:** Uses `workflow_definition` in some places and `workflow_def` in others.

---

### 17. Missing Type Annotations
**File:** `tools/function-tools.mdx`  
**Line:** 211  
**Issue:** Uses `any` instead of `Any` from typing.

**Current Code:**
```python
def process_users(...) -> Dict[str, any]:  # ❌ Should be Any
```

**Fix:**
```python
from typing import Dict, Any

def process_users(...) -> Dict[str, Any]:
```

---

### 18. Incomplete Error Handling Example
**File:** `sdk/client/overview.mdx`  
**Line:** 252  
**Issue:** References `invalid_workflow` variable that's never defined.

**Current Code:**
```python
try:
    workflow_result = client.workflows.execute(invalid_workflow)  # ❌ Undefined
except WorkflowExecutionError as e:
    print(f"Workflow execution failed: {e}")
```

---

## Recommendations

### Immediate Fixes Required:
1. ✅ Update all references from `Kubiya` to `KubiyaClient`
2. ✅ Remove all references to `AsyncKubiya` (doesn't exist)
3. ✅ Add missing imports (json, uuid, time, datetime, asyncio)
4. ✅ Fix `concurrent.futures` in requirements
5. ✅ Update exception import paths
6. ✅ Add complete imports to MCP examples

### Documentation Improvements:
1. 📝 Verify all API methods exist in the actual SDK
2. 📝 Ensure consistency in variable naming across examples
3. 📝 Add "Prerequisites" section to examples requiring imports
4. 📝 Include complete, runnable code examples
5. 📝 Cross-reference with actual SDK exports in `__init__.py`

### Testing Recommendations:
1. 🧪 Create automated tests that run all documentation examples
2. 🧪 Add CI/CD pipeline to validate Python code blocks
3. 🧪 Use tools like `doctest` to verify examples
4. 🧪 Implement linting for code blocks in markdown

---

## Files with Most Issues

| File | Critical | Warning | Minor | Total |
|------|----------|---------|-------|-------|
| `quickstart/sdk-quickstart.mdx` | 4 | 3 | 1 | 8 |
| `tutorials/ai-powered-automation.mdx` | 1 | 4 | 1 | 6 |
| `sdk/client/overview.mdx` | 0 | 2 | 2 | 4 |
| `mcpserver/overview.mdx` | 1 | 0 | 0 | 1 |
| `tools/function-tools.mdx` | 1 | 0 | 1 | 2 |
| `sdk/workflow-dsl/overview.mdx` | 0 | 0 | 1 | 1 |

---

## Validation Methodology

This report was created by:
1. Reading 16+ documentation files from `docs/kubiya/`
2. Extracting all Python code blocks
3. Cross-referencing with actual SDK source code in `kubiya/`
4. Checking imports against `kubiya/__init__.py`
5. Verifying class and method existence via grep searches
6. Identifying logical errors and missing dependencies

---

## Next Steps

1. **Priority 1:** Fix all critical issues (🔴) - these break code execution
2. **Priority 2:** Address warning issues (🟡) - these cause confusion
3. **Priority 3:** Clean up minor issues (🟢) - improve quality
4. **Long-term:** Implement automated documentation testing

---

**Report Generated By:** AI Analysis Tool  
**SDK Version Analyzed:** Based on current main branch  
**Last Updated:** 2025-10-04

