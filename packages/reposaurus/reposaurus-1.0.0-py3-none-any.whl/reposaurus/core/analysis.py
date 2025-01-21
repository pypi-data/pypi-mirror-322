"""Repository analysis functionality."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import os

@dataclass
class RepositoryMetrics:
    """Container for repository analysis metrics."""
    total_files: int = 0
    files_by_type: Dict[str, int] = None
    total_tokens: int = 0
    total_lines: int = 0

    def __post_init__(self):
        if self.files_by_type is None:
            self.files_by_type = {}

class RepositoryAnalyzer:
    """Analyzes repository contents and generates metrics."""

    def __init__(self):
        """Initialize the repository analyzer."""
        self.metrics = RepositoryMetrics()
        
    def analyze_file(self, path: Path) -> None:
        """
        Analyze a single file and update metrics.
        
        Args:
            path: Path to the file to analyze
        """
        if not path.is_file():
            return
            
        # Update file type statistics
        extension = path.suffix.lower()
        if not extension:
            extension = '(no extension)'
        self.metrics.files_by_type[extension] = self.metrics.files_by_type.get(extension, 0) + 1
        self.metrics.total_files += 1
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple token estimation (split by whitespace)
                self.metrics.total_tokens += len(content.split())
                self.metrics.total_lines += content.count('\n') + 1
        except (UnicodeDecodeError, IOError):
            # Skip binary files
            pass
            
    def get_metrics(self) -> RepositoryMetrics:
        """Get the current repository metrics."""
        return self.metrics

    def format_metrics(self) -> str:
        """Format metrics for output."""
        lines = [
            "Repository Analysis:",
            f"Total Files Processed: {self.metrics.total_files}",
            "\nFile Type Breakdown:",
        ]
        
        for ext, count in sorted(self.metrics.files_by_type.items()):
            lines.append(f"  {ext}: {count} files")
            
        lines.extend([
            f"\nEstimated Tokens: {self.metrics.total_tokens:,}",
            f"Lines of Code: {self.metrics.total_lines:,}"
        ])
        
        return "\n".join(lines)