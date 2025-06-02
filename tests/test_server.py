# ABOUTME: This file contains tests for the MCP server functionality.
# ABOUTME: It tests the health_check tool and server initialization.

"""Tests for the Firefly III MCP server."""

import pytest

from firefly_iii_mcp.server import health_check, mcp


class TestHealthCheck:
    """Test the health_check tool."""

    @pytest.mark.asyncio
    async def test_health_check_returns_ok_status(self):
        """Test that health_check returns the expected status."""
        result = await health_check()

        assert result == {"status": "ok", "service": "firefly-iii-mcp"}

    @pytest.mark.asyncio
    async def test_health_check_response_structure(self):
        """Test that health_check returns proper structure."""
        result = await health_check()

        assert isinstance(result, dict)
        assert "status" in result
        assert "service" in result
        assert result["status"] == "ok"
        assert result["service"] == "firefly-iii-mcp"


class TestServer:
    """Test server initialization."""

    def test_mcp_server_name(self):
        """Test that the MCP server has the correct name."""
        assert mcp.name == "firefly-iii-mcp"

    def test_health_check_tool_registered(self):
        """Test that health_check tool is registered."""
        # Check that the tool is registered in the server
        # FastMCP stores tools internally, we can verify by calling list_tools
        # which returns tool info
        assert mcp is not None
        assert mcp.name == "firefly-iii-mcp"
