# ABOUTME: This file contains utility functions and helper classes used throughout the package.
# ABOUTME: It includes error handling, data formatting, and common operations.

"""Utility functions and helper classes."""

import logging
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# Custom exceptions
class FireflyError(Exception):
    """Base exception for Firefly III related errors."""
    pass


class FireflyAuthError(FireflyError):
    """Authentication error with Firefly III API."""
    pass


class FireflyValidationError(FireflyError):
    """Validation error for API requests."""
    pass


class FireflyNotFoundError(FireflyError):
    """Resource not found error."""
    pass


class FireflyServerError(FireflyError):
    """Server error from Firefly III API."""
    pass


class FireflyRateLimitError(FireflyError):
    """Rate limit exceeded error."""
    pass