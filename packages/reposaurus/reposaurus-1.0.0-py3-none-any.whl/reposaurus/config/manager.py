"""Configuration management for Reposaurus."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from .patterns import (
    DEFAULT_CONFIG,
    DEFAULT_EXCLUDE_PATTERNS,
    SECRET_PATTERNS,
    DEFAULT_ALLOWLIST
)


class ConfigurationError(Exception):
    """Raised when there are configuration-related errors."""
    pass


class ConfigManager:
    """Manages Reposaurus configuration loading and validation."""

    DEFAULT_CONFIG_FILE = ".reposaurus.yml"

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config = DEFAULT_CONFIG.copy()

        if Path(self.config_file).exists():
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._merge_config(user_config)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing config file: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Error loading config file: {str(e)}")

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user configuration with defaults."""

        def deep_merge(target, source):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    deep_merge(target[key], value)
                else:
                    target[key] = value

        deep_merge(self.config, user_config)

    def get_exclude_patterns(self) -> List[str]:
        """Get combined exclude patterns from defaults and config."""
        patterns = []

        if self.config['patterns']['use_default_ignores']:
            patterns.extend(DEFAULT_EXCLUDE_PATTERNS)

        patterns.extend(self.config['patterns'].get('additional_excludes', []))
        return patterns

    def get_secret_patterns(self) -> Dict[str, str]:
        """Get combined secret detection patterns."""
        patterns = SECRET_PATTERNS.copy()

        # Add custom patterns
        patterns.update(self.config['detect_secrets'].get('patterns', {}))

        # Remove excluded patterns
        for pattern in self.config['detect_secrets'].get('exclude_patterns', []):
            patterns.pop(pattern, None)

        return patterns

    def get_allowlist(self) -> Dict[str, List[str]]:
        """Get combined allowlist from defaults and config."""
        allowlist = DEFAULT_ALLOWLIST.copy()

        # Merge with custom allowlist
        for file_path, patterns in self.config['detect_secrets'].get('allowlist', {}).items():
            if file_path in allowlist:
                allowlist[file_path].extend(patterns)
            else:
                allowlist[file_path] = patterns

        return allowlist

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self.config[section][key]
        except KeyError:
            return default