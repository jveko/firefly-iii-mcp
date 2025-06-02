# ABOUTME: This file defines all MCP tools that expose Firefly III functionality.
# ABOUTME: It implements tools for each resource type with action-based routing.

"""MCP tool definitions for Firefly III resources."""

import logging
from typing import Optional, List, Dict, Any

from .server import mcp

logger = logging.getLogger(__name__)


# Tools will be implemented here in subsequent steps