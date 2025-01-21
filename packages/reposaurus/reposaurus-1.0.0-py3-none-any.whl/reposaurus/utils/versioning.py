"""Utilities for managing versioned output files."""

import re
from pathlib import Path
from typing import Optional, Tuple
import datetime
from ..config.manager import ConfigManager


class VersionManager:
    """Manages versioning of output files."""

    def __init__(self, config: Optional[ConfigManager] = None):
        """Initialize version manager."""
        self.config = config or ConfigManager()
        self.versioning_config = self.config.get('output', 'versioning', {})

    def get_versioned_path(self, base_path: Path) -> Path:
        """Get the appropriate versioned path based on configuration."""
        if not self.versioning_config.get('enabled', True):
            return base_path

        version_format = self.versioning_config.get('format', 'numeric')
        if version_format == 'none':
            return base_path
        elif version_format == 'date':
            return self._get_date_versioned_path(base_path)
        else:  # numeric
            return self._get_numeric_versioned_path(base_path)

    def _get_date_versioned_path(self, base_path: Path) -> Path:
        """Generate a date-based version path."""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        stem, suffix = base_path.stem, base_path.suffix
        versioned_name = f"{stem}_{timestamp}{suffix}"
        return base_path.parent / versioned_name

    def _get_numeric_versioned_path(self, base_path: Path) -> Path:
        """Generate a numerically versioned path."""
        if not base_path.exists() and self.versioning_config.get('start_fresh', False):
            return self._get_versioned_name(base_path, 1)

        # Find existing versions
        stem, suffix = base_path.stem, base_path.suffix
        parent = base_path.parent
        base_pattern = f"{stem}_v*{suffix}"

        max_version = 0
        for file in parent.glob(base_pattern):
            version = self._parse_version_from_filename(file.name)
            if version is not None:
                max_version = max(max_version, version)

        # Determine next version
        if max_version == 0 and base_path.exists():
            next_version = 2  # First versioned file after base
        else:
            next_version = max_version + 1 if max_version > 0 else 1

        return self._get_versioned_name(base_path, next_version)

    def _get_versioned_name(self, base_path: Path, version: int) -> Path:
        """Generate a versioned filename."""
        stem, suffix = base_path.stem, base_path.suffix
        versioned_name = f"{stem}_v{version}{suffix}"
        return base_path.parent / versioned_name

    def _parse_version_from_filename(self, filename: str) -> Optional[int]:
        """Extract version number from a filename."""
        match = re.search(r'_v(\d+)\.', filename)
        return int(match.group(1)) if match else None