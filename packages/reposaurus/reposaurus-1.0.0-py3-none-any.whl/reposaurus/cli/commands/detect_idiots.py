"""Implementation of the detect-idiots command for finding sensitive information."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Pattern
import yaml
from ..commands.base import Command, register_command
from ...config.manager import ConfigManager
from ...core.exclusions import ExclusionManager
from ...utils.filesystem import safe_read_file
from ...core.secrets import SecretDetector


@register_command
class DetectIdiotsCommand(Command):
    """Command for detecting potential secrets in repository files."""

    name = "detect-idiots"
    help = "Scan repository for potential secrets and sensitive information"
    description = "Analyze repository contents to detect potential secrets, API keys, and other sensitive information"

    @classmethod
    def configure_parser(cls, parser):
        """Configure command-specific arguments."""
        parser.add_argument('path',
                            nargs='?',
                            default='.',
                            help='Repository path to scan (default: current directory)')
        parser.add_argument('--config',
                            '-c',
                            help='Path to configuration file')
        parser.add_argument('--output',
                            '-o',
                            help='Write results to file instead of stdout')
        parser.add_argument('--quiet',
                            '-q',
                            action='store_true',
                            help='Only output findings, no additional info')

    def execute(self, args):
        """Execute the detect-idiots command."""
        try:
            repo_path = Path(args.path).resolve()
            if not repo_path.is_dir():
                raise ValueError(f"Error: {args.path} is not a directory")

            # Initialize configuration and managers
            config = ConfigManager(args.config)
            detector = SecretDetector(config)
            exclusions = ExclusionManager(repo_path)

            findings = []

            # Process all files
            for path in sorted(repo_path.rglob('*')):
                if path.is_file() and not exclusions.should_exclude(path):
                    content = safe_read_file(path)
                    if content is not None:
                        rel_path = path.relative_to(repo_path)
                        file_findings = detector.scan_content(content, str(rel_path))
                        findings.extend(file_findings)

            # Output results
            if findings:
                if args.output:
                    with open(args.output, 'w') as f:
                        yaml.dump(findings, f)
                    print(f"Results written to {args.output}")
                else:
                    if not args.quiet:
                        print("\nPotential secrets found:")
                        print("-" * 50)

                    for finding in findings:
                        print(f"Type: {finding['type']}")
                        print(f"File: {finding['file']}")
                        print(f"Line: {finding['line']}")
                        print(f"Match: {finding['text']}")
                        print("-" * 50)

                return 1  # Return error code if secrets found
            else:
                if not args.quiet:
                    print("No potential secrets found. Good job! 🎉")
                return 0

        except Exception as e:
            print(f"Error: {str(e)}")
            return 1