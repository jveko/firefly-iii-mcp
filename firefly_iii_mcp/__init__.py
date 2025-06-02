# ABOUTME: This file initializes the firefly_iii_mcp package and exports key components.
# ABOUTME: It defines the package version and makes core functionality easily importable.

"""Firefly III MCP Server - Model Context Protocol server for Firefly III personal finance manager."""

__version__ = "0.1.0"

from .server import mcp, serve

__all__ = ["mcp", "serve", "__version__"]