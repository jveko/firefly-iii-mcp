# ABOUTME: This file implements the HTTP client for the Firefly III API.
# ABOUTME: It handles authentication, request/response processing, and error management.

"""Firefly III API client using httpx."""

import logging
import os

import httpx

logger = logging.getLogger(__name__)


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
