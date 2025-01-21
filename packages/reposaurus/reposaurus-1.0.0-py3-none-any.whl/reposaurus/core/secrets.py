"""Core functionality for detecting secrets and sensitive information."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Pattern


class SecretDetector:
    """Detects potential secrets and sensitive information in files."""

    def __init__(self, config):
        """Initialize the detector with patterns from config."""
        self.config = config
        self.patterns = self.config.get_secret_patterns()
        self.single_line_patterns = {}
        self.multi_line_patterns = {}
        self._compile_patterns()
        self.excluded_files = self._get_excluded_files()

    def _compile_patterns(self) -> None:
        """Compile regex patterns and separate them into single and multiline."""
        single_line = {}
        multi_line = {}

        for name, pattern in self.patterns.items():
            if 'CERTIFICATE' in pattern or 'PRIVATE KEY' in pattern:
                multi_line[name] = re.compile(pattern, re.MULTILINE | re.DOTALL)
            else:
                single_line[name] = re.compile(pattern, re.MULTILINE)

        self.single_line_patterns = single_line
        self.multi_line_patterns = multi_line

    def _get_excluded_files(self) -> List[str]:
        """Get list of files to exclude from scanning."""
        allowlist = self.config.get_allowlist()
        excluded = []

        for file_path in allowlist:
            # If the value is an empty list, the entire file should be excluded
            if isinstance(allowlist[file_path], list) and len(allowlist[file_path]) == 0:
                excluded.append(file_path)
            # Handle directory wildcards
            if file_path.endswith('/'):
                excluded.append(file_path + '*')
            # Handle exact file paths
            if not file_path.endswith('/') and file_path not in excluded:
                excluded.append(file_path)

        return excluded

    def _should_exclude_file(self, filename: str) -> bool:
        """Check if file should be completely excluded from scanning."""
        norm_filename = str(Path(filename))
        allowlist = self.config.get_allowlist()

        # Special handling for configuration and documentation files
        special_files = [
            'reposaurus/config/patterns/__init__.py',
            'reposaurus/cli/commands/init_config.py',
            '.reposaurus.yml'
        ]
        if norm_filename in special_files:
            return True

        # Check for files with empty allowlist
        for file_path, patterns in allowlist.items():
            if isinstance(patterns, list) and len(patterns) == 0:
                if norm_filename == file_path:
                    return True
                if file_path.endswith('/') and norm_filename.startswith(file_path):
                    return True

        return False

    def _should_allow(self, content: str, filename: str, allowlist: Dict[str, List[str]]) -> bool:
        """Check if content should be allowed based on filename and content."""
        # First check if the file should be completely excluded
        if self._should_exclude_file(filename):
            return True

        # Normalize the filename for matching
        norm_filename = str(Path(filename))

        # Check exact file matches
        if filename in allowlist and content.strip() in allowlist[filename]:
            return True

        # Check normalized file matches
        if norm_filename in allowlist and content.strip() in allowlist[norm_filename]:
            return True

        # Check directory wildcards
        for allow_path, patterns in allowlist.items():
            if allow_path.endswith('/'):
                allow_dir = allow_path.rstrip('/')
                if filename.startswith(allow_dir) or norm_filename.startswith(allow_dir):
                    if content.strip() in patterns:
                        return True

        return False

    def _find_line_number(self, content: str, match: str) -> int:
        """Find the line number where a match starts."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if match in line:
                return i
        return 1  # fallback to first line if not found

    def scan_content(self, content: str, filename: str) -> List[Dict]:
        """
        Scan content for potential secrets.

        Args:
            content: The content to scan
            filename: Name of the file being scanned

        Returns:
            List of found secrets with type, line number, and matched text
        """
        # First check if the entire file should be excluded
        if self._should_exclude_file(filename):
            return []

        findings = []
        allowlist = self.config.get_allowlist()

        # First check multiline patterns on the entire content
        for pattern_name, pattern in self.multi_line_patterns.items():
            matches = pattern.finditer(content)
            for match in matches:
                matched_text = match.group(0)
                if not self._should_allow(matched_text, filename, allowlist):
                    findings.append({
                        'type': pattern_name,
                        'file': filename,
                        'line': self._find_line_number(content, matched_text.split('\n')[0]),
                        'text': matched_text
                    })
        # Then check single line patterns line by line
        for i, line in enumerate(content.splitlines(), 1):

            for pattern_name, pattern in self.single_line_patterns.items():
                matches = pattern.finditer(line)
                for match in matches:
                    if self._should_allow(match.group(0), filename, allowlist):
                        continue

                    findings.append({
                        'type': pattern_name,
                        'file': filename,
                        'line': i,
                        'text': match.group(0)
                    })

        return findings