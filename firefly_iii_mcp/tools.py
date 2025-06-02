# ABOUTME: This file defines all MCP tools that expose Firefly III functionality.
# ABOUTME: It implements tools for each resource type with action-based routing.

"""MCP tool definitions for Firefly III resources."""

import logging

logger = logging.getLogger(__name__)


@mcp.tool()
async def check_connection() -> Dict[str, Any]:
    """Test API connectivity and authentication to Firefly III.
    
    Returns connection status, API version, and user information.
    Provides helpful error messages for common issues.
    """
    from .client import FireflyClient, FireflyConnectionError, FireflyAuthError
    
    logger.info("Checking connection to Firefly III API...")
    
    try:
        # Test that environment variables are set
        import os
        base_url = os.getenv("FIREFLY_URL")
        token = os.getenv("FIREFLY_TOKEN")
        
        if not base_url:
            return {
                "status": "error",
                "error": "FIREFLY_URL environment variable is not set",
                "help": "Set FIREFLY_URL to your Firefly III instance URL (e.g., https://firefly.example.com)"
            }
        
        if not token:
            return {
                "status": "error", 
                "error": "FIREFLY_TOKEN environment variable is not set",
                "help": "Set FIREFLY_TOKEN to your personal access token from Firefly III"
            }
        
        # Create client and test connection
        async with FireflyClient() as client:
            # Test the about endpoint
            about_data = await client.test_connection()
            
            # Get user info
            user_data = await client.get("/api/v1/about/user")
            
            return {
                "status": "success",
                "connection": {
                    "base_url": base_url,
                    "api_version": about_data.get("data", {}).get("api_version", "unknown"),
                    "firefly_version": about_data.get("data", {}).get("version", "unknown"),
                },
                "user": {
                    "email": user_data.get("data", {}).get("attributes", {}).get("email", "unknown"),
                    "role": user_data.get("data", {}).get("attributes", {}).get("role", "unknown"),
                },
                "message": "Successfully connected to Firefly III"
            }
            
    except FireflyAuthError as e:
        return {
            "status": "error",
            "error": str(e),
            "help": "Check that your personal access token is valid and has not expired"
        }
    except FireflyConnectionError as e:
        return {
            "status": "error",
            "error": str(e),
            "help": "Check that FIREFLY_URL is correct and the server is accessible"
        }
    except Exception as e:
        logger.error(f"Unexpected error during connection check: {e}", exc_info=True)
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "help": "Check the logs for more details"
        }


@mcp.tool()
async def get_server_info() -> Dict[str, Any]:
    """Retrieve detailed information about the Firefly III server.
    
    Returns version info, API capabilities, and server configuration.
    """
    from .client import FireflyClient, FireflyError
    
    logger.info("Getting server information...")
    
    try:
        async with FireflyClient() as client:
            # Get basic about info
            about_data = await client.get("/api/v1/about")
            
            # Get system configuration
            config_data = await client.get("/api/v1/configuration")
            
            # Extract relevant information
            about_attrs = about_data.get("data", {})
            config_attrs = config_data.get("data", {})
            
            return {
                "server": {
                    "version": about_attrs.get("version", "unknown"),
                    "api_version": about_attrs.get("api_version", "unknown"),
                    "php_version": about_attrs.get("php_version", "unknown"),
                    "os": about_attrs.get("os", "unknown"),
                    "driver": about_attrs.get("driver", "unknown"),
                },
                "configuration": {
                    "is_demo": config_attrs.get("is_demo_site", False),
                    "authentication": config_attrs.get("authentication_guard", "unknown"),
                    "permissions": config_attrs.get("permission_update_check", -1),
                    "last_update_check": config_attrs.get("last_update_check", "unknown"),
                    "single_user_mode": config_attrs.get("single_user_mode", False),
                },
                "capabilities": {
                    "webhooks": "webhooks" in about_attrs.get("api_url", ""),
                    "rules": "rules" in about_attrs.get("api_url", ""),
                    "recurring": "recurring" in about_attrs.get("api_url", ""),
                }
            }
            
    except FireflyError as e:
        logger.error(f"Failed to get server info: {e}")
        return {
            "error": str(e),
            "help": "Ensure you have a valid connection to Firefly III"
        }
    except Exception as e:
        logger.error(f"Unexpected error getting server info: {e}", exc_info=True)
        return {
            "error": f"Unexpected error: {str(e)}"
        }


@mcp.tool()
async def configure_auth(
    url: Optional[str] = None,
    token: Optional[str] = None,
    test: bool = True
) -> Dict[str, Any]:
    """Validate and test Firefly III authentication configuration.
    
    Args:
        url: Firefly III instance URL (uses FIREFLY_URL env var if not provided)
        token: Personal access token (uses FIREFLY_TOKEN env var if not provided)
        test: Whether to test the connection after configuration
        
    Returns diagnostic information about the authentication setup.
    """
    import os
    from urllib.parse import urlparse
    from .client import FireflyClient, FireflyError
    
    logger.info("Configuring authentication...")
    
    # Get values from parameters or environment
    base_url = url or os.getenv("FIREFLY_URL", "")
    api_token = token or os.getenv("FIREFLY_TOKEN", "")
    
    result = {
        "configuration": {},
        "validation": {},
        "test_result": None
    }
    
    # Check URL
    if not base_url:
        result["validation"]["url"] = {
            "status": "error",
            "message": "No URL provided. Set FIREFLY_URL environment variable or pass url parameter"
        }
    else:
        # Validate URL format
        try:
            parsed = urlparse(base_url)
            if not parsed.scheme:
                result["validation"]["url"] = {
                    "status": "error",
                    "message": "URL must include protocol (http:// or https://)"
                }
            elif parsed.scheme not in ["http", "https"]:
                result["validation"]["url"] = {
                    "status": "error",
                    "message": f"Invalid protocol: {parsed.scheme}. Use http or https"
                }
            else:
                result["validation"]["url"] = {
                    "status": "success",
                    "message": f"Valid URL format: {base_url}"
                }
                result["configuration"]["url"] = base_url
        except Exception as e:
            result["validation"]["url"] = {
                "status": "error",
                "message": f"Invalid URL format: {str(e)}"
            }
    
    # Check token
    if not api_token:
        result["validation"]["token"] = {
            "status": "error",
            "message": "No token provided. Set FIREFLY_TOKEN environment variable or pass token parameter"
        }
    else:
        # Basic token validation
        if len(api_token) < 10:
            result["validation"]["token"] = {
                "status": "warning",
                "message": "Token seems too short. Ensure you're using a valid personal access token"
            }
        else:
            result["validation"]["token"] = {
                "status": "success",
                "message": f"Token provided (length: {len(api_token)})"
            }
        result["configuration"]["token_length"] = len(api_token)
    
    # Test connection if requested and both values are provided
    if test and base_url and api_token:
        logger.info("Testing authentication...")
        try:
            async with FireflyClient(base_url=base_url, token=api_token) as client:
                about_data = await client.test_connection()
                result["test_result"] = {
                    "status": "success",
                    "message": "Authentication successful",
                    "server_version": about_data.get("data", {}).get("version", "unknown")
                }
        except FireflyError as e:
            result["test_result"] = {
                "status": "error",
                "message": str(e),
                "type": type(e).__name__
            }
        except Exception as e:
            result["test_result"] = {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "type": type(e).__name__
            }
    
    # Provide environment variable info
    result["environment"] = {
        "FIREFLY_URL": "set" if os.getenv("FIREFLY_URL") else "not set",
        "FIREFLY_TOKEN": "set" if os.getenv("FIREFLY_TOKEN") else "not set"
    }
    
    return result