"""Core repository processing functionality with configuration support."""

from pathlib import Path
from typing import Dict, Any, Optional, List

from ..utils.filesystem import is_binary_file, safe_read_file
from .exclusions import ExclusionManager
from .output import OutputHandler
from ..config.manager import ConfigManager
from ..utils.versioning import VersionManager
from .analysis import RepositoryAnalyzer


class RepositoryProcessor:
    """Handles the processing of repository contents."""

    def __init__(self, repo_path: Path, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the repository processor.

        Args:
            repo_path: Path to the repository
            options: Processing options including exclusion patterns and config settings
        """
        # Ensure we have absolute paths
        self.repo_path = Path(repo_path).resolve()
        self.options = options or {}

        # Initialize configuration and managers
        self.config = ConfigManager(self.options.get('config_file'))
        self.version_manager = VersionManager(self.config)

        # Initialize exclusions with configuration
        self.exclusions = ExclusionManager(
            repo_path=self.repo_path,
            exclude_file=self.options.get('exclude_file') or
                         self.config.get('patterns', 'ignore_file_path'),
            additional_excludes=self.config.get('patterns', 'additional_excludes', []),
            command_line_excludes=self.options.get('exclude')
        )

        self.analyzer = RepositoryAnalyzer()
        self.show_analysis = options.get('show_analysis', False) if options else False

    def get_output_path(self, base_name: str = None) -> Path:
        """
        Generate output path based on configuration.

        Args:
            base_name: Optional base name for the output file. If not provided,
                      uses template from configuration.

        Returns:
            Path: Configured and versioned output path
        """
        if base_name is None:
            template = self.config.get('output', 'filename_template',
                                       '{repo_name}_repository_contents')
            base_name = template.format(repo_name=self.repo_path.name)

        # Resolve output directory relative to repository root
        output_dir = self.config.get('output', 'directory', '.')
        if output_dir == '.':
            base_path = self.repo_path / f"{base_name}.txt"
        else:
            base_path = self.repo_path / output_dir / f"{base_name}.txt"

        # Get versioned path if enabled
        output_path = self.version_manager.get_versioned_path(base_path)

        # Handle git integration if configured
        if self.config.get('git', 'auto_update_gitignore', True):
            self._update_gitignore(output_path)

        return output_path

    def _update_gitignore(self, output_path: Path) -> None:
        """
        Update .gitignore with the pattern for repository content files.

        Args:
            output_path: Example output path to derive the pattern from
        """
        gitignore_path = self.repo_path / '.gitignore'
        try:
            # Get the base pattern from the configuration
            template = self.config.get('output', 'filename_template',
                                       '{repo_name}_repository_contents')
            base_name = template.format(repo_name=self.repo_path.name)

            # Create the pattern that will match all versioned files
            if self.version_manager.versioning_config.get('format') == 'date':
                pattern = f"{base_name}_*.txt"
            else:  # numeric or none
                pattern = f"{base_name}*.txt"  # This will catch both base and versioned files

            # Get the relative directory if output is not in repo root
            output_dir = self.config.get('output', 'directory', '.')
            if output_dir != '.':
                pattern = str(Path(output_dir) / pattern)

            # Normalize path separators
            pattern = pattern.replace('\\', '/')

            # Create .gitignore if it doesn't exist
            if not gitignore_path.exists():
                gitignore_path.write_text(f"{pattern}\n", encoding='utf-8')
                return

            # Read existing patterns
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f.readlines() if line.strip()]

            # Add new pattern if not present
            if pattern not in patterns:
                patterns.append(pattern)

                # Write back with consistent formatting
                with open(gitignore_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(patterns) + '\n')

        except Exception as e:
            print(f"Warning: Could not update .gitignore: {str(e)}")

    def get_repository_info(self) -> Dict[str, str]:
        """Get repository information including path and configuration."""
        info = {
            'name': self.repo_path.name,
            'absolute_path': str(self.repo_path.absolute()),
            'relative_path': str(self.repo_path)  # Use str() directly for test compatibility
        }
        
        # Add command-line exclusions if present
        if self.options.get('exclude'):
            info['command_line_excludes'] = self.options['exclude']
            
        return info

    def get_directory_structure(self) -> List[str]:
        """
        Generate directory structure as a list of paths.

        Returns:
            List of paths in the directory structure, with directories marked with trailing slash
        """
        structure = []

        try:
            # Use rglob to recursively find all files and directories
            for path in sorted(self.repo_path.rglob('*')):
                # Skip excluded paths
                if self.exclusions.should_exclude(path):
                    continue

                try:
                    # Get path relative to repository root
                    rel_path = path.relative_to(self.repo_path)

                    # Add trailing slash for directories
                    if path.is_dir():
                        structure.append(f"{str(rel_path)}/")
                    else:
                        structure.append(str(rel_path))
                except ValueError:
                    # Skip paths that can't be made relative
                    continue
        except Exception as e:
            print(f"Warning: Error processing directory structure: {str(e)}")

        return structure

    def process_file(self, path: Path, output_handler: OutputHandler) -> None:
        """
        Process a single file.

        Args:
            path: Path to the file to process
            output_handler: Handler for writing output
        """
        try:
            # Skip binary files
            if is_binary_file(path):
                return

            # Read file contents
            content = safe_read_file(path)
            if content is not None:
                rel_path = path.relative_to(self.repo_path)
                output_handler.write_file(rel_path, content)

                # Analyze the file if not excluded
                if not self.exclusions.should_exclude(path):
                    self.analyzer.analyze_file(path)
        except Exception as e:
            print(f"Warning: Could not process {path}: {str(e)}")

    def process(self, output_handler: Optional[OutputHandler] = None) -> None:
        """
        Process the repository and write contents.

        Args:
            output_handler: Optional handler for writing repository contents.
                        If not provided, creates one using configured output path.
        """
        try:
            # Create output handler if not provided
            if output_handler is None:
                output_path = self.get_output_path()
                output_handler = OutputHandler(output_path, self.config)

            with output_handler:
                # Write repository information
                repo_info = self.get_repository_info()
                output_handler.write_repository_info(repo_info)

                # Process all files first to collect analysis
                for path in sorted(self.repo_path.rglob('*')):
                    if path.is_file() and not self.exclusions.should_exclude(path):
                        self.analyzer.analyze_file(path)

                # Write repository analysis
                if output_handler:
                    output_handler.write_section("Repository Analysis", self.analyzer.format_metrics())
                if self.show_analysis:
                    print("\n" + self.analyzer.format_metrics())

                # Write directory structure
                structure = self.get_directory_structure()
                output_handler.write_structure(structure)

                # Process and write all files
                for path in sorted(self.repo_path.rglob('*')):
                    if path.is_file() and not self.exclusions.should_exclude(path):
                        self.process_file(path, output_handler)

        except Exception as e:
            print(f"Error processing repository: {str(e)}")
            raise