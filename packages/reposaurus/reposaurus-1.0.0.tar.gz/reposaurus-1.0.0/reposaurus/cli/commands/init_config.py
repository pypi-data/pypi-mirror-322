"""Implementation of the init-config command."""

import argparse
from pathlib import Path
import yaml
from ..commands.base import Command, register_command
from ...config.patterns import DEFAULT_CONFIG


def write_file_if_allowed(path: Path, content: str, force: bool = False) -> None:
    """Write content to file if it doesn't exist or force is True."""
    if path.exists() and not force:
        raise FileExistsError(
            f"Error: {path} already exists. Use --force to overwrite."
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


@register_command
class InitConfigCommand(Command):
    """Command for initializing a Reposaurus configuration file."""

    name = "init-config"
    help = "Create a default Reposaurus configuration file"
    description = "Initialize a new .reposaurus.yml with default configuration including secret detection settings"

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--force', '-f',
                            action='store_true',
                            help='Overwrite existing config file if it exists')
        parser.add_argument('--output', '-o',
                            default='.reposaurus.yml',
                            help='Output file path (default: .reposaurus.yml)')

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the init-config command."""
        try:
            output_path = Path(args.output)

            # Start with a copy of the default config
            config = DEFAULT_CONFIG.copy()

            # Add example patterns to the detect_secrets section
            config['detect_secrets']['allowlist'] = {
                "tests/": [
                    'API_KEY = "TEST_KEY"',
                    'PASSWORD = "TEST_PASSWORD"'
                ],
                "examples/config.py": [
                    'API_KEY = "EXAMPLE_KEY"'
                ]
            }

            config['detect_secrets']['patterns'] = {
                "custom_api_key": '(?i)my_api_key["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]*'
            }

            config['detect_secrets']['exclude_patterns'] = [
                "password"  # Excludes default password pattern
            ]

            # Generate the configuration content with comments
            content = [
                "# Reposaurus Configuration File",
                "",
                "# File processing and exclusion settings",
                yaml.dump({"patterns": config["patterns"]}, default_flow_style=False, sort_keys=False),
                "",
                "# Output file formatting and versioning",
                yaml.dump({"output": config["output"]}, default_flow_style=False, sort_keys=False),
                "",
                "# Git integration settings",
                yaml.dump({"git": config["git"]}, default_flow_style=False, sort_keys=False),
                "",
                "# Secret detection settings",
                "# These settings control the detect-idiots command",
                "# Add custom patterns and allowlists here",
                yaml.dump({"detect_secrets": config["detect_secrets"]}, default_flow_style=False, sort_keys=False),
                ""
            ]

            write_file_if_allowed(output_path, '\n'.join(content), args.force)
            print(f"Created Reposaurus configuration file at {output_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to create config file: {str(e)}")