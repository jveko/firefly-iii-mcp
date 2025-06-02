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


@mcp.tool()
async def health_check() -> dict[str, str]:
    """Check the health status of the Firefly III MCP server.
    
    Returns a simple status indicating the server is running.
    This tool can be used to verify the MCP server is responsive.
    
    Returns:
        Dict containing status and service name
    """
    logger.debug("Health check requested")
    return {"status": "ok", "service": "firefly-iii-mcp"}

