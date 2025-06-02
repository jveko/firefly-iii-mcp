# ABOUTME: This file implements the FastMCP server that handles all MCP protocol communication.
# ABOUTME: It initializes the server, registers tools, and manages the server lifecycle.

"""FastMCP server implementation for Firefly III."""

import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("firefly-iii-mcp")


def serve():
    """Start the MCP server."""
    logger.info("Starting Firefly III MCP server...")
    # Server will be started by FastMCP when tools are registered
    return 0