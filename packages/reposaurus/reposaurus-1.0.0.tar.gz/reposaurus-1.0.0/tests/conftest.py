"""Shared pytest fixtures for Reposaurus tests."""

import os
import tempfile
from pathlib import Path
import shutil
import pytest


def pytest_configure(config):
    """
    Configure pytest for parallel execution.
    Initialize any shared resources in a thread-safe manner.
    """
    # Ensure the base temp directory exists
    base_temp = Path(tempfile.gettempdir()) / "reposaurus-tests"
    base_temp.mkdir(exist_ok=True)

    # Configure logging to prevent interference between workers
    import logging
    logging.basicConfig(format='%(asctime)s [%(worker_id)s] %(levelname)s: %(message)s')


@pytest.fixture(scope='function')
def temp_dir(request):
    """Create a worker-specific temporary directory for test files."""
    # Get the worker id, default to 'master' for non-parallel runs
    worker_id = request.config.workerinput.get('workerid', 'master')

    # Create a worker-specific temp directory
    base_temp = Path(tempfile.gettempdir()) / "reposaurus-tests"
    worker_temp = base_temp / f"worker-{worker_id}"
    worker_temp.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir=str(worker_temp)) as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(scope='function')
def sample_repo(temp_dir):
    """Create a sample repository structure for testing."""
    # Create test files
    (temp_dir / "file1.txt").write_text("Test content 1")
    (temp_dir / "file2.py").write_text("print('Test content 2')")

    # Create a nested directory
    nested_dir = temp_dir / "nested"
    nested_dir.mkdir()
    (nested_dir / "file3.txt").write_text("Test content 3")

    # Create a .git directory (empty)
    (temp_dir / ".git").mkdir()

    return temp_dir

@pytest.fixture(scope='function')
def sample_config(temp_dir):
    """Create a sample configuration file."""
    config_content = """
patterns:
    use_default_ignores: true
    ignore_file_path: .reposaurusignore
    additional_excludes: []
output:
    filename_template: "{repo_name}_repository_contents"
    directory: "."
    versioning:
        enabled: true
        format: numeric
git:
    auto_update_gitignore: true
detect_secrets:
    patterns: {}
    exclude_patterns: []
    allowlist: {}
"""
    config_file = temp_dir / ".reposaurus.yml"
    config_file.write_text(config_content)
    return config_file