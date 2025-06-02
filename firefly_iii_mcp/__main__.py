# ABOUTME: This file enables running the package as a module with python -m firefly_iii_mcp.
# ABOUTME: It imports and executes the main server function to start the MCP server.

"""Entry point for running the Firefly III MCP server."""

import sys
from .server import serve


def main():
    """Main entry point for the CLI."""
    return serve()


if __name__ == "__main__":
    sys.exit(main())