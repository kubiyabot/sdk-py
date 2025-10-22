"""Kubiya MCP Server - Legacy compatibility wrapper.

This module provides backward compatibility. 
Use kubiya.mcp.server package directly for new code.
"""

import warnings
from kubiya.mcp.server.core import (
    KubiyaMCPServer,
    create_server
)

warnings.warn(
    "Importing from kubiya.mcp.server is deprecated. "
    "Use kubiya.mcp.server package directly.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy exports
__all__ = [
    "KubiyaMCPServer",
    "create_server"
]
