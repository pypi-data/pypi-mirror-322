"""Output handling and formatting for repository contents."""

from pathlib import Path
from typing import Dict, List, Union, Optional
import datetime

from ..utils.filesystem import ensure_directory
from ..utils.formatting import format_path
from ..config.manager import ConfigManager


class OutputHandler:
    """Handles the formatting and writing of repository contents."""

    SEPARATOR_STYLES = {
        'line': ('=' * 48, '-' * 48),
        'double-line': ('=' * 48, '-' * 48),
        'hash': ('#' * 48, '-' * 48),
        'none': ('', '')
    }

    def __init__(self, output_path: Path, config: Optional[ConfigManager] = None):
        """Initialize the output handler."""
        self.output_path = Path(output_path)
        self.config = config or ConfigManager()
        ensure_directory(self.output_path.parent)
        self.file = None

        # Get separator style from config
        style = self.config.get('output', 'section_separator', 'line')
        length = self.config.get('output', 'separator_length', 48)
        self.section_sep, self.subsection_sep = self._get_separators(style, length)

    def _get_separators(self, style: str, length: int) -> tuple[str, str]:
        """Get section separators based on configuration."""
        if style not in self.SEPARATOR_STYLES:
            style = 'line'
        main, sub = self.SEPARATOR_STYLES[style]
        return main[:length], sub[:length]

    def __enter__(self):
        """Context manager entry."""
        self.file = open(self.output_path, 'w', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.file:
            self.file.close()
            self.file = None

    def _ensure_open(self):
        """Ensure the output file is open."""
        if not self.file:
            self.file = open(self.output_path, 'w', encoding='utf-8')

    def write(self, content: str) -> None:
        """Write content to the output file."""
        self._ensure_open()
        self.file.write(content)
        self.file.write('\n')

    def write_section(self, title: str, content: Optional[str] = None) -> None:
        """Write a formatted section with title and optional content."""
        self.write("")
        self.write(self.section_sep)
        self.write(f"# {title}")
        self.write(self.subsection_sep)
        if content:
            self.write("")
            self.write(content)
        self.write("")

    def write_repository_info(self, info: Dict[str, str]) -> None:
        """Write repository information section including config settings."""
        content = [
            f"Name: {info['name']}",
            f"Absolute Path: {info['absolute_path']}",
            f"Relative Path: {info['relative_path']}",
            "",
            "Configuration Settings:",
            f"Use Default Ignores: {self.config.get('patterns', 'use_default_ignores', True)}",
            f"Ignore File: {self.config.get('patterns', 'ignore_file_path', '.reposaurusignore')}",
            f"Output Directory: {self.config.get('output', 'directory', '.')}",
            f"Versioning: {self.config.get('output', 'versioning', {}).get('format', 'numeric')}"
        ]

        # Add command-line exclusions if present
        if 'command_line_excludes' in info:
            content.extend([
                "",
                "Command-Line Exclusions:",
                f"Excluded Patterns: {info['command_line_excludes']}"
            ])

        content.extend([
            "",
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])
        
        self.write_section("Repository Information", '\n'.join(content))

    def write_structure(self, structure: List[str]) -> None:
        """Write directory structure section."""
        content = '\n'.join(f"    {path}" for path in structure)
        self.write_section("Directory Structure", content)

    def write_file(self, rel_path: Union[str, Path], content: str) -> None:
        """Write a file's contents with appropriate formatting."""
        self.write_section(f"File: {format_path(rel_path)}", content)

    def close(self) -> None:
        """Close the output file if it's open."""
        if self.file:
            self.file.close()
            self.file = None