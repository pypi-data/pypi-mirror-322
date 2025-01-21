"""Implementation of the init-ignore command for creating default ignore files."""

import argparse
from pathlib import Path
from typing import Dict, List, Set
from ..commands.base import Command, register_command
from ...config.patterns import DEFAULT_EXCLUDE_PATTERNS


def write_file_if_allowed(path: Path, content: str, force: bool = False) -> None:
    """Write content to file if it doesn't exist or force is True."""
    if path.exists() and not force:
        raise FileExistsError(
            f"Error: {path} already exists. Use --force to overwrite."
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def categorize_pattern(pattern: str) -> str:
    """Determine the most appropriate category for a pattern."""
    if pattern.endswith('/'):
        if any(x in pattern for x in ['.git', '.svn', '.vs', '.idea', '.vscode']):
            return "IDE and Version Control"
        if any(x in pattern for x in ['__pycache__', '.pytest_cache']):
            return "Cache and Temporary Files"
        if any(x in pattern for x in ['build', 'dist', 'eggs', 'wheels']):
            return "Build and Distribution"
        if any(x in pattern for x in ['node_modules', 'bower_components']):
            return "Dependencies"
        if any(x in pattern for x in ['env', 'venv', '.env', '.venv']):
            return "Virtual Environments"
        return "Other Directories"

    # File patterns
    if any(x in pattern for x in ['.pyc', '.pyo', '.pyd', '.egg-info', '.egg']):
        return "Python Artifacts"
    if any(x in pattern for x in ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.mp3', '.mp4', '.avi', '.mov']):
        return "Media Files"
    if any(x in pattern for x in ['.zip', '.tar', '.gz', '.rar', '.7z']):
        return "Archives"
    if any(x in pattern for x in ['.swp', '.swo', '.DS_Store', 'Thumbs.db']):
        return "System and Editor Files"
    if any(x in pattern for x in ['.log', '.sqlite', '.db']):
        return "Logs and Databases"
    if '_repository_contents' in pattern:
        return "Reposaurus Output"

    return "Other"


@register_command
class InitIgnoreCommand(Command):
    """Command for initializing a Reposaurus ignore file."""

    name = "init-ignore"
    help = "Create a default Reposaurus ignore file for excluding files and directories"
    description = "Initialize a new .reposaurusignore file with default exclusion patterns"

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--force', '-f',
                            action='store_true',
                            help='Overwrite existing ignore file if it exists')
        parser.add_argument('--output', '-o',
                            default='.reposaurusignore',
                            help='Output file path (default: .reposaurusignore)')

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the init-ignore command."""
        try:
            output_path = Path(args.output)

            # Categorize patterns
            patterns_by_category: Dict[str, Set[str]] = {}
            for pattern in DEFAULT_EXCLUDE_PATTERNS:
                category = categorize_pattern(pattern)
                if category not in patterns_by_category:
                    patterns_by_category[category] = set()
                patterns_by_category[category].add(pattern)

            # Generate the ignore file content
            content = [
                "# Reposaurus Ignore File",
                "# Patterns for excluding files and directories from processing",
                "# Uses .gitignore syntax",
                "",
            ]

            # Define category order
            category_order = [
                "IDE and Version Control",
                "Virtual Environments",
                "Python Artifacts",
                "Build and Distribution",
                "Dependencies",
                "Cache and Temporary Files",
                "System and Editor Files",
                "Media Files",
                "Archives",
                "Logs and Databases",
                "Reposaurus Output",
                "Other Directories",
                "Other"
            ]

            # Add each category with its patterns
            for category in category_order:
                if category in patterns_by_category and patterns_by_category[category]:
                    content.extend([
                        f"# {category}",
                        *sorted(patterns_by_category[category]),
                        ""
                    ])

            content.extend([
                "# Custom Exclusions",
                "# Add your custom exclusion patterns below",
                ""
            ])

            write_file_if_allowed(output_path, '\n'.join(content), args.force)
            print(f"Created Reposaurus ignore file at {output_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to create ignore file: {str(e)}")