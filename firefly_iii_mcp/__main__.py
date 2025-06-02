# ABOUTME: This file enables running the package as python -m firefly_iii_mcp.
# ABOUTME: It imports and executes the main server function to start the MCP server.

"""Entry point for running the Firefly III MCP server."""

from .server import mcp


def main():
    """Main entry point for the CLI."""
    # FastMCP handles the execution when called directly
    mcp.run()


if __name__ == "__main__":
    main()

