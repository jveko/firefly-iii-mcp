# ABOUTME: This file defines Pydantic models for all Firefly III data structures.
# ABOUTME: It provides type safety and validation for API requests and responses.

"""Data models and type definitions for Firefly III resources."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field


# Base models and enums will be implemented here in subsequent steps