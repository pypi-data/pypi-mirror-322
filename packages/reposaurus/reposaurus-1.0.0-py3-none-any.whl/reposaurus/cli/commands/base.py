"""Base command infrastructure and registry for Reposaurus CLI."""

import argparse
from abc import ABC, abstractmethod
from typing import Dict, Type, List

# Command registry
_commands: Dict[str, Type['Command']] = {}


def register_command(cls: Type['Command']) -> Type['Command']:
    """Register a command class in the global registry."""
    _commands[cls.name] = cls
    return cls


def get_command(name: str) -> Type['Command']:
    """Get a command class by name."""
    if name not in _commands:
        raise ValueError(f"Unknown command: {name}")
    return _commands[name]


def get_commands() -> List[Type['Command']]:
    """Get all registered command classes."""
    return list(_commands.values())


class Command(ABC):
    """Base class for all Reposaurus commands."""

    name: str = None  # Command name used in CLI
    help: str = None  # Short help message
    description: str = None  # Longer help message for command help

    @classmethod
    def add_parser(cls, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """Add this command's parser to the subparsers."""
        if not cls.name or not cls.help:
            raise ValueError(f"Command {cls.__name__} must define 'name' and 'help'")

        parser = subparsers.add_parser(
            cls.name,
            help=cls.help,
            description=cls.description or cls.help
        )
        cls.configure_parser(parser)
        return parser

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Configure command-specific arguments."""
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> None:
        """Execute the command."""
        raise NotImplementedError()