# ABOUTME: This file implements the HTTP client for the Firefly III API.
# ABOUTME: It handles authentication, request/response processing, and error management.

"""Firefly III API client using httpx."""

import logging
import os

import httpx

logger = logging.getLogger(__name__)


# Custom Exceptions
class FireflyError(Exception):
    """Base exception for Firefly III client errors."""
    pass


class FireflyAuthError(FireflyError):
    """Raised when authentication fails."""
    pass


class FireflyConnectionError(FireflyError):
    """Raised when connection to Firefly III fails."""
    pass


class FireflyAPIError(FireflyError):
    """Raised when Firefly III API returns an error."""
    def __init__(self, message: str, status_code: int, response_body: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class FireflyClient:
    """HTTP client for Firefly III API."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        """Initialize the Firefly III client.
        
        Args:
            base_url: The base URL of the Firefly III instance
            token: The personal access token for authentication
        """
        self.base_url = (base_url or os.getenv("FIREFLY_URL", "")).rstrip("/")
        self.token = token or os.getenv("FIREFLY_TOKEN", "")

        if not self.base_url:
            raise ValueError("FIREFLY_URL environment variable is required")
        if not self.token:
            raise ValueError("FIREFLY_TOKEN environment variable is required")

        # Initialize httpx client with auth headers
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate errors.
        
        Args:
            response: The HTTP response from the API
            
        Returns:
            The JSON response data
            
        Raises:
            FireflyAuthError: For 401/403 responses
            FireflyAPIError: For other error responses
        """
        # Log request/response details
        logger.debug(
            f"{response.request.method} {response.url} - Status: {response.status_code}"
        )
        
        if response.status_code == 401:
            raise FireflyAuthError("Authentication failed. Check your API token.")
        elif response.status_code == 403:
            raise FireflyAuthError("Permission denied. Check your API token permissions.")
        elif response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get("message", f"API error: {response.status_code}")
            except Exception:
                message = f"API error: {response.status_code}"
                error_data = None
            raise FireflyAPIError(message, response.status_code, error_data)
        
        try:
            return response.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise FireflyAPIError("Invalid JSON response from API", response.status_code)
    
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API.
        
        Args:
            path: The API endpoint path (e.g., "/api/v1/accounts")
            params: Optional query parameters
            
        Returns:
            The JSON response data
        """
        try:
            response = await self.client.get(path, params=params)
            return self._handle_response(response)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise FireflyConnectionError(f"Failed to connect to {self.base_url}")
        except httpx.TimeoutException:
            logger.error("Request timed out")
            raise FireflyConnectionError("Request timed out")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise FireflyConnectionError(f"HTTP error: {e}")
    
    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request to the API.
        
        Args:
            path: The API endpoint path
            json: The JSON data to send
            
        Returns:
            The JSON response data
        """
        try:
            response = await self.client.post(path, json=json)
            return self._handle_response(response)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise FireflyConnectionError(f"Failed to connect to {self.base_url}")
        except httpx.TimeoutException:
            logger.error("Request timed out")
            raise FireflyConnectionError("Request timed out")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise FireflyConnectionError(f"HTTP error: {e}")
    
    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request to the API.
        
        Args:
            path: The API endpoint path
            json: The JSON data to send
            
        Returns:
            The JSON response data
        """
        try:
            response = await self.client.put(path, json=json)
            return self._handle_response(response)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise FireflyConnectionError(f"Failed to connect to {self.base_url}")
        except httpx.TimeoutException:
            logger.error("Request timed out")
            raise FireflyConnectionError("Request timed out")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise FireflyConnectionError(f"HTTP error: {e}")
    
    async def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request to the API.
        
        Args:
            path: The API endpoint path
            json: The JSON data to send
            
        Returns:
            The JSON response data
        """
        try:
            response = await self.client.patch(path, json=json)
            return self._handle_response(response)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise FireflyConnectionError(f"Failed to connect to {self.base_url}")
        except httpx.TimeoutException:
            logger.error("Request timed out")
            raise FireflyConnectionError("Request timed out")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise FireflyConnectionError(f"HTTP error: {e}")
    
    async def delete(self, path: str) -> Dict[str, Any]:
        """Make a DELETE request to the API.
        
        Args:
            path: The API endpoint path
            
        Returns:
            The JSON response data (usually empty for deletes)
        """
        try:
            response = await self.client.delete(path)
            # DELETE often returns 204 No Content
            if response.status_code == 204:
                return {"success": True}
            return self._handle_response(response)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise FireflyConnectionError(f"Failed to connect to {self.base_url}")
        except httpx.TimeoutException:
            logger.error("Request timed out")
            raise FireflyConnectionError("Request timed out")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise FireflyConnectionError(f"HTTP error: {e}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Firefly III by calling the /api/v1/about endpoint.
        
        Returns:
            The API about information
            
        Raises:
            FireflyConnectionError: If connection fails
            FireflyAuthError: If authentication fails
        """
        logger.info("Testing connection to Firefly III API...")
        try:
            result = await self.get("/api/v1/about")
            logger.info("Connection successful!")
            return result
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            raise