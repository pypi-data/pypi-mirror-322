"""Pattern matching and file exclusion management."""

from pathlib import Path
from typing import Optional, List
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from ..config.patterns import DEFAULT_EXCLUDE_PATTERNS


class ExclusionManager:
    """Manages file exclusion patterns and matching."""

    def __init__(self, repo_path: Optional[Path] = None, exclude_file: Optional[str] = None,
                 additional_excludes: Optional[List[str]] = None, command_line_excludes: Optional[str] = None):
        """
        Initialize the exclusion manager.

        Args:
            repo_path: Root path of the repository (defaults to current directory)
            exclude_file: Optional path to a custom exclusion file
            additional_excludes: Optional list of additional patterns to exclude
            command_line_excludes: Optional comma-separated string of exclusion patterns from command line
        """
        self.repo_path = repo_path.resolve() if repo_path else Path.cwd().resolve()
        self.exclude_file = exclude_file
        self.additional_excludes = additional_excludes or []
        self.command_line_excludes = []

        # Parse command-line exclusions if provided
        if command_line_excludes:
            self.command_line_excludes = [
                pattern.strip() for pattern in command_line_excludes.split(',')
                if pattern.strip()
            ]

        # If no exclude file specified, look for .reposaurusignore in repo root
        if not exclude_file:
            repo_ignore = self.repo_path / '.reposaurusignore'
            if repo_ignore.exists():
                self.exclude_file = str(repo_ignore)

        self.spec = self._create_path_spec()

    def _create_path_spec(self) -> PathSpec:
        """Create a PathSpec object from exclusion patterns."""
        patterns = []

        # Add default patterns
        patterns.extend(DEFAULT_EXCLUDE_PATTERNS)

        # Add patterns from exclude file if it exists
        if self.exclude_file and Path(self.exclude_file).exists():
            try:
                with open(self.exclude_file, 'r', encoding='utf-8') as f:
                    file_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    patterns.extend(file_patterns)
            except Exception as e:
                print(f"Warning: Could not read exclusion patterns from {self.exclude_file}: {str(e)}")

        # Add additional excludes
        if self.additional_excludes:
            patterns.extend(self.additional_excludes)

        # Add command-line excludes (these take precedence)
        if self.command_line_excludes:
            patterns.extend(self.command_line_excludes)

        # Create PathSpec object
        return PathSpec.from_lines(GitWildMatchPattern, patterns)

    def should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded based on patterns.

        Args:
            path: Path to check

        Returns:
            True if the path should be excluded
        """
        try:
            # For symlinks, use the symlink path instead of the resolved path
            actual_path = path.absolute()
            if actual_path.is_symlink():
                actual_path = Path(actual_path)
            else:
                actual_path = actual_path.resolve()

            # Get path relative to repository root
            try:
                rel_path = str(actual_path.relative_to(self.repo_path))
            except ValueError:
                # If path is outside repository, exclude it
                return True

            # Normalize path separators for consistent matching
            normalized_path = rel_path.replace('\\', '/')
            
            # Add trailing slash for directories to ensure proper matching
            if path.is_dir() and not normalized_path.endswith('/'):
                normalized_path += '/'

            # Check if the path matches any pattern
            is_excluded = self.spec.match_file(normalized_path)
            
            # If not excluded directly, check if any parent directory is excluded
            if not is_excluded:
                parts = Path(normalized_path).parts
                for i in range(len(parts)):
                    parent_path = '/'.join(parts[:i+1])
                    if not parent_path.endswith('/'):
                        parent_path += '/'
                    if self.spec.match_file(parent_path):
                        return True
            
            return is_excluded

        except Exception as e:
            # Log warning but don't halt processing
            print(f"Warning: Error checking exclusion for {path}: {str(e)}")
            return False