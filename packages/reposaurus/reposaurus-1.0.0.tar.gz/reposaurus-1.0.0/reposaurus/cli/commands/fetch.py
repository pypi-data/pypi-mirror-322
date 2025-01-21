"""Implementation of the fetch command for repository content extraction."""

import argparse
import os
from pathlib import Path

from .base import Command, register_command
from ...core.processor import RepositoryProcessor
from ...core.output import OutputHandler
from ...config.manager import ConfigManager
from ...utils.versioning import VersionManager


@register_command
class FetchCommand(Command):
    """Command for fetching repository contents."""

    name = "fetch"
    help = "Create a text snapshot of your repository"
    description = "Process repository and create a comprehensive text snapshot"

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Configure fetch command arguments."""
        parser.add_argument('path',
                          nargs='?',
                          default=os.getcwd(),
                          help='Repository path (default: current directory)')
        parser.add_argument('--exclude-file',
                          '-e',
                          help='Path to custom exclusion file (uses .gitignore syntax)')
        parser.add_argument('--exclude',
                          '-x',
                          help='Comma-separated list of files/directories to exclude (e.g., logs/,temp.txt)')
        parser.add_argument('--output',
                          '-o',
                          help='Output file path (default: repository_contents.txt)')
        parser.add_argument('--config',
                          '-c',
                          help='Path to configuration file (default: .reposaurus.yml)')
        parser.add_argument('--show-analysis',
                    '-sa',
                    action='store_true',
                    help='Show repository analysis metrics in terminal output')

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the fetch command."""
        try:
            # Validate repository path
            repo_path = Path(args.path)
            if not repo_path.is_dir():
                raise ValueError(f"Error: {args.path} is not a directory")
            if not os.access(repo_path, os.R_OK):
                raise PermissionError(f"Error: No read permission for {args.path}")

            # Setup options with configuration
            options = {
                'exclude_file': args.exclude_file,
                'config_file': args.config,
                'exclude': args.exclude,
                'show_analysis': args.show_analysis
            }

            # Initialize processor
            processor = RepositoryProcessor(repo_path, options)

            # Generate output path
            if args.output:
                base_output_path = Path(args.output)
                output_path = base_output_path
            else:
                output_path = processor.get_output_path()

            # Check output path permissions
            if output_path.exists() and not os.access(output_path, os.W_OK):
                raise PermissionError(f"Error: No write permission for {output_path}")

            # Ensure output directory exists and is writable
            output_dir = output_path.parent
            if not output_dir.exists():
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    raise IOError(f"Error: Could not create output directory: {str(e)}")
            elif not os.access(output_dir, os.W_OK):
                raise PermissionError(f"Error: No write permission for directory {output_dir}")

            # Validate exclude file if provided
            if args.exclude_file:
                exclude_path = Path(args.exclude_file)
                if not exclude_path.is_file():
                    raise ValueError(f"Error: Exclusion file {args.exclude_file} not found")
                if not os.access(exclude_path, os.R_OK):
                    raise PermissionError(f"Error: No read permission for {args.exclude_file}")

            # Process repository
            output_handler = OutputHandler(output_path, processor.config)
            processor.process(output_handler)

            print(f"\nRepository contents written to {output_path}")

        except (ValueError, PermissionError, IOError) as e:
            # Re-raise expected errors with their original messages
            raise
        except Exception as e:
            # Wrap unexpected errors with a more user-friendly message
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")
