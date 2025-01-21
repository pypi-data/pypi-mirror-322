"""Command handlers for Reposaurus CLI."""

from .base import Command, register_command, get_command, get_commands
from .fetch import FetchCommand
from .init_ignore import InitIgnoreCommand
from .init_config import InitConfigCommand
from .detect_idiots import DetectIdiotsCommand

__all__ = [
    'Command',
    'register_command',
    'get_command',
    'get_commands',
    'FetchCommand',
    'InitIgnoreCommand',
    'InitConfigCommand',
    'DetectIdiotsCommand',
]