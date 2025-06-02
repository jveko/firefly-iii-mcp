# ABOUTME: This file initializes the firefly_iii_mcp package and exports key components.
# ABOUTME: It defines the package version and makes core functionality importable.

"""Firefly III MCP Server - MCP server for Firefly III personal finance manager."""

__version__ = "0.1.0"

from .server import mcp

__all__ = ["mcp", "__version__"]

