# ABOUTME: This file contains comprehensive tests for the Firefly III API client.
# ABOUTME: It tests authentication, HTTP methods, error handling, and connection functionality.

"""Tests for the Firefly III API client."""

import os
import pytest
import httpx
from unittest.mock import MagicMock, patch
from firefly_iii_mcp.client import (
    FireflyClient,
    FireflyError,
    FireflyAuthError,
    FireflyConnectionError,
    FireflyAPIError,
)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        "FIREFLY_URL": "https://firefly.example.com",
        "FIREFLY_TOKEN": "test-token-123"
    }):
        yield


@pytest.fixture
async def client(mock_env_vars):
    """Create a FireflyClient instance for testing."""
    async with FireflyClient() as client:
        yield client


class TestFireflyClientInit:
    """Test client initialization."""
    
    def test_init_with_env_vars(self, mock_env_vars):
        """Test initialization with environment variables."""
        client = FireflyClient()
        assert client.base_url == "https://firefly.example.com"
        assert client.token == "test-token-123"
    
    def test_init_with_params(self):
        """Test initialization with parameters."""
        client = FireflyClient(
            base_url="https://custom.firefly.com",
            token="custom-token"
        )
        assert client.base_url == "https://custom.firefly.com"
        assert client.token == "custom-token"
    
    def test_init_removes_trailing_slash(self):
        """Test that trailing slashes are removed from base URL."""
        client = FireflyClient(
            base_url="https://firefly.example.com/",
            token="token"
        )
        assert client.base_url == "https://firefly.example.com"
    
    def test_init_missing_url(self):
        """Test initialization fails without URL."""
        with pytest.raises(ValueError, match="FIREFLY_URL"):
            FireflyClient(token="token")
    
    def test_init_missing_token(self):
        """Test initialization fails without token."""
        with pytest.raises(ValueError, match="FIREFLY_TOKEN"):
            FireflyClient(base_url="https://firefly.example.com")


class TestFireflyClientMethods:
    """Test HTTP methods."""
    
    @pytest.mark.asyncio
    async def test_get_success(self, client):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "get", return_value=mock_response) as mock_get:
            mock_get.return_value = mock_response
            result = await client.get("/api/v1/accounts")
            assert result == {"data": "test"}
    
    @pytest.mark.asyncio
    async def test_post_success(self, client):
        """Test successful POST request."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "123", "created": True}
        mock_response.request.method = "POST"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "post", return_value=mock_response):
            result = await client.post("/api/v1/accounts", json={"name": "Test"})
            assert result == {"id": "123", "created": True}
    
    @pytest.mark.asyncio
    async def test_put_success(self, client):
        """Test successful PUT request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": True}
        mock_response.request.method = "PUT"
        mock_response.url = "https://firefly.example.com/api/v1/accounts/123"
        
        with patch.object(client.client, "put", return_value=mock_response):
            result = await client.put("/api/v1/accounts/123", json={"name": "Updated"})
            assert result == {"updated": True}
    
    @pytest.mark.asyncio
    async def test_patch_success(self, client):
        """Test successful PATCH request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"patched": True}
        mock_response.request.method = "PATCH"
        mock_response.url = "https://firefly.example.com/api/v1/accounts/123"
        
        with patch.object(client.client, "patch", return_value=mock_response):
            result = await client.patch("/api/v1/accounts/123", json={"balance": 100})
            assert result == {"patched": True}
    
    @pytest.mark.asyncio
    async def test_delete_success(self, client):
        """Test successful DELETE request."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.request.method = "DELETE"
        mock_response.url = "https://firefly.example.com/api/v1/accounts/123"
        
        with patch.object(client.client, "delete", return_value=mock_response):
            result = await client.delete("/api/v1/accounts/123")
            assert result == {"success": True}
    
    @pytest.mark.asyncio
    async def test_delete_with_body(self, client):
        """Test DELETE request that returns a body."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"deleted": True, "id": "123"}
        mock_response.request.method = "DELETE"
        mock_response.url = "https://firefly.example.com/api/v1/accounts/123"
        
        with patch.object(client.client, "delete", return_value=mock_response):
            result = await client.delete("/api/v1/accounts/123")
            assert result == {"deleted": True, "id": "123"}


class TestFireflyClientErrors:
    """Test error handling."""
    
    @pytest.mark.asyncio
    async def test_auth_error_401(self, client):
        """Test 401 authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "get", return_value=mock_response):
            with pytest.raises(FireflyAuthError, match="Authentication failed"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_auth_error_403(self, client):
        """Test 403 permission denied error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "get", return_value=mock_response):
            with pytest.raises(FireflyAuthError, match="Permission denied"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_api_error_with_message(self, client):
        """Test API error with error message in response."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid request data"}
        mock_response.request.method = "POST"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "post", return_value=mock_response):
            with pytest.raises(FireflyAPIError) as exc_info:
                await client.post("/api/v1/accounts", json={})
            
            assert "Invalid request data" in str(exc_info.value)
            assert exc_info.value.status_code == 400
            assert exc_info.value.response_body == {"message": "Invalid request data"}
    
    @pytest.mark.asyncio
    async def test_api_error_invalid_json(self, client):
        """Test API error when response is not valid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "get", return_value=mock_response):
            with pytest.raises(FireflyAPIError, match="API error: 500"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_connection_error(self, client):
        """Test connection error."""
        with patch.object(client.client, "get", side_effect=httpx.ConnectError("Connection failed")):
            with pytest.raises(FireflyConnectionError, match="Failed to connect"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_timeout_error(self, client):
        """Test timeout error."""
        with patch.object(client.client, "get", side_effect=httpx.TimeoutException("Timeout")):
            with pytest.raises(FireflyConnectionError, match="Request timed out"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_http_error(self, client):
        """Test generic HTTP error."""
        with patch.object(client.client, "get", side_effect=httpx.HTTPError("HTTP error")):
            with pytest.raises(FireflyConnectionError, match="HTTP error"):
                await client.get("/api/v1/accounts")
    
    @pytest.mark.asyncio
    async def test_invalid_json_response(self, client):
        """Test handling of invalid JSON in successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/accounts"
        
        with patch.object(client.client, "get", return_value=mock_response):
            with pytest.raises(FireflyAPIError, match="Invalid JSON response"):
                await client.get("/api/v1/accounts")


class TestFireflyClientConnection:
    """Test connection functionality."""
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, client):
        """Test successful connection test."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "version": "5.7.0",
                "api_version": "1.5.0",
                "php_version": "8.1.0"
            }
        }
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/about"
        
        with patch.object(client.client, "get", return_value=mock_response):
            result = await client.test_connection()
            assert result["data"]["version"] == "5.7.0"
    
    @pytest.mark.asyncio
    async def test_test_connection_auth_failure(self, client):
        """Test connection test with auth failure."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.request.method = "GET"
        mock_response.url = "https://firefly.example.com/api/v1/about"
        
        with patch.object(client.client, "get", return_value=mock_response):
            with pytest.raises(FireflyAuthError):
                await client.test_connection()
    
    @pytest.mark.asyncio
    async def test_test_connection_network_failure(self, client):
        """Test connection test with network failure."""
        with patch.object(client.client, "get", side_effect=httpx.ConnectError("Network error")):
            with pytest.raises(FireflyConnectionError):
                await client.test_connection()


class TestFireflyClientContextManager:
    """Test async context manager functionality."""
    
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_env_vars):
        """Test using client as async context manager."""
        async with FireflyClient() as client:
            assert isinstance(client, FireflyClient)
            assert client.base_url == "https://firefly.example.com"
    
    @pytest.mark.asyncio
    async def test_close_method(self, client):
        """Test close method."""
        from unittest.mock import AsyncMock
        mock_aclose = AsyncMock()
        client.client.aclose = mock_aclose
        
        await client.close()
        mock_aclose.assert_called_once()