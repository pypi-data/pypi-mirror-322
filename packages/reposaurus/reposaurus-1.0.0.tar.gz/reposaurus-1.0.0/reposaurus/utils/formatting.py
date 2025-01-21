"""Text formatting utility functions."""

from pathlib import Path
from typing import Union


def format_path(path: Union[str, Path]) -> str:
    """
    Format a path for display, ensuring forward slashes and proper relative paths.

    Args:
        path: Path to format

    Returns:
        Formatted path string
    """
    return str(Path(path)).replace('\\', '/')


def format_size(size_bytes: int) -> str:
    """
    Format a file size in bytes to human readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human readable size string (e.g., "1.23 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            if unit == 'B':
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def indent_text(text: str, spaces: int = 4) -> str:
    """
    Indent each line of text by specified number of spaces.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent

    Returns:
        Indented text
    """
    if not text:
        return text

    indent = ' ' * spaces
    lines = text.splitlines(keepends=True)
    return ''.join(indent + line if line.strip() else line
                   for line in lines)