"""Configuration module for Reposaurus."""

from .patterns import (
    DEFAULT_CONFIG,
    DEFAULT_EXCLUDE_PATTERNS,
    SECRET_PATTERNS,
    DEFAULT_ALLOWLIST
)
from .manager import ConfigManager

__all__ = [
    'ConfigManager',
    'DEFAULT_CONFIG',
    'DEFAULT_EXCLUDE_PATTERNS',
    'SECRET_PATTERNS',
    'DEFAULT_ALLOWLIST'
]