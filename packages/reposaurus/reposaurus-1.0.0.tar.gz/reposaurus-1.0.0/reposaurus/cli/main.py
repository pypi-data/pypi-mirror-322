"""Main entry point for the Reposaurus CLI."""

import argparse
import sys
from typing import Optional, Sequence

from . import commands


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description='Reposaurus - Repository to Text Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Add version information
    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {__import__("reposaurus").__version__}')

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Register commands
    for command_cls in commands.get_commands():
        command_cls.add_parser(subparsers)

    return parser


def handle_legacy_command(args: Sequence[str]) -> argparse.Namespace:
    """Handle the legacy command format for backward compatibility."""
    parsed_args = argparse.Namespace()
    parsed_args.command = 'fetch'
    parsed_args.path = args[0] if len(args) > 0 else None
    parsed_args.exclude_file = None
    parsed_args.output = None
    return parsed_args


def main(args: Optional[Sequence[str]] = None) -> None:
    """
    Main entry point for the CLI.

    Args:
        args: Command line arguments (uses sys.argv if not provided)
    """
    parser = create_parser()
    if args is None:
        args = sys.argv[1:]

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Default to 'fetch' command if no command specified (backward compatibility)
    if not parsed_args.command and len(args) > 0:
        parsed_args = handle_legacy_command(args)

    # If still no command, default to fetch with current directory
    if not parsed_args.command:
        parsed_args = handle_legacy_command([])

    try:
        # Get the command class and execute
        command_cls = commands.get_command(parsed_args.command)
        command = command_cls()
        command.execute(parsed_args)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()