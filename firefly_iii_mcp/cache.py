# ABOUTME: This file implements caching functionality to improve API performance.
# ABOUTME: It provides TTL-based caching with configurable expiration and invalidation.

"""Caching implementation for Firefly III API responses."""

import logging
from collections import OrderedDict
from typing import Any

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple TTL-based cache manager."""

    def __init__(self, default_ttl: int = 300):
        """Initialize cache with default TTL in seconds."""
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._max_size = 1000  # Maximum cache entries
