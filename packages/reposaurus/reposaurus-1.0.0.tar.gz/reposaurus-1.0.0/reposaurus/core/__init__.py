"""Core functionality for Reposaurus."""

from .processor import RepositoryProcessor
from .output import OutputHandler
from .exclusions import ExclusionManager
from .secrets import SecretDetector

__all__ = [
    'RepositoryProcessor',
    'OutputHandler',
    'ExclusionManager',
    'SecretDetector'
]