# ABOUTME: This file implements the FastMCP server for MCP protocol communication.
# ABOUTME: It initializes the server, registers tools, and manages the server lifecycle.

"""FastMCP server implementation for Firefly III."""

import logging

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("firefly-iii-mcp")

# Import tools to register them with the server
from . import tools


def serve():
    """Start the MCP server."""
    logger.info("Starting Firefly III MCP server...")
    # Run the FastMCP server
    mcp.run()
    return 0