"""Integration tests for CLI command outputs and formatting."""

import pytest
from pathlib import Path
import yaml
from unittest.mock import patch
import re
import time
from reposaurus.cli.main import main


@pytest.fixture
def sample_repo(tmp_path):
    """Create a sample repository with diverse content."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()

    # Create standard files
    (repo_dir / "README.md").write_text("# Test Project\nSample project for testing")
    (repo_dir / "setup.py").write_text('version = "1.0.0"\nsetup(name="test")')

    # Create nested structure
    src = repo_dir / "src"
    src.mkdir()
    (src / "main.py").write_text("def main():\n    print('Hello')")
    (src / "__init__.py").touch()

    tests = repo_dir / "tests"
    tests.mkdir()
    (tests / "test_main.py").write_text("def test_main():\n    assert True")

    return repo_dir


def test_fetch_output_structure(sample_repo, monkeypatch):
    """Test fetch command output structure and formatting."""
    monkeypatch.chdir(str(sample_repo))

    with patch("sys.argv", ["reposaurus", "fetch"]):
        main()

    # Add small delay to ensure file system catches up
    time.sleep(0.1)

    output_files = list(sample_repo.glob("*repository_contents*.txt"))
    assert len(output_files) > 0
    content = output_files[0].read_text()

    # Verify sections are properly formatted
    sections = content.split("================================================")
    assert len(sections) >= 3  # At least repo info, structure, and one file

    # Check repository info section
    info_section = sections[1]
    assert "# Repository Information" in info_section
    assert "Name:" in info_section
    assert "Configuration Settings:" in info_section
    assert "Generated:" in info_section

    # Verify structure formatting
    assert "src/" in content
    assert "tests/" in content
    assert "__init__.py" in content

    # Check file content sections are properly separated
    assert re.search(r"# File: .*?README\.md", content)
    assert "# Test Project" in content