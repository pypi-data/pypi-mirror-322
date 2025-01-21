"""Integration tests for the Reposaurus CLI commands."""

import os
import pytest
from pathlib import Path
import yaml
from unittest.mock import patch
import sys
import subprocess
from reposaurus.cli.main import main

@pytest.fixture
def temp_repo(temp_dir):
    """Create a temporary repository structure for testing."""
    # Create test files
    (temp_dir / "file1.txt").write_text("Test content 1")
    (temp_dir / "file2.py").write_text("print('Test content 2')")

    # Create nested directory with test files
    nested_dir = temp_dir / "nested"
    nested_dir.mkdir()
    (nested_dir / "file3.txt").write_text("Test content 3")

    # Add test secrets
    (nested_dir / "config.py").write_text("""
API_KEY = "1234567890abcdef"
TEST_API_KEY = "TEST_KEY"
PASSWORD = "super_secure_123!"
""")

    return temp_dir


def test_fetch_command_basic(temp_repo, monkeypatch):
    """Test basic fetch command functionality."""
    monkeypatch.chdir(temp_repo)

    with patch("sys.argv", ["reposaurus", "fetch"]):
        main()

    output_files = list(temp_repo.glob("*repository_contents*.txt"))
    assert len(output_files) > 0

    content = output_files[0].read_text()
    assert "# Repository Information" in content
    assert "# Directory Structure" in content
    assert "Test content 1" in content


def test_fetch_command_with_config(temp_repo, monkeypatch):
    """Test fetch command with custom configuration."""
    monkeypatch.chdir(temp_repo)

    config = {
        "output": {
            "filename_template": "custom_snapshot",
            "directory": "output",
            "versioning": {"enabled": True, "format": "numeric"}
        }
    }

    config_file = temp_repo / ".reposaurus.yml"
    output_dir = temp_repo / "output"
    output_dir.mkdir()

    with open(config_file, "w") as f:
        yaml.dump(config, f)

    with patch("sys.argv", ["reposaurus", "fetch"]):
        main()

    assert any(Path(output_dir).glob("custom_snapshot*.txt"))


def test_init_config_command(temp_repo, monkeypatch):
    """Test initialization of configuration file."""
    monkeypatch.chdir(temp_repo)

    with patch("sys.argv", ["reposaurus", "init-config"]):
        main()

    config_file = temp_repo / ".reposaurus.yml"
    assert config_file.exists()

    config = yaml.safe_load(config_file.read_text())
    assert all(key in config for key in ["patterns", "output", "detect_secrets"])


def test_init_ignore_command(temp_repo, monkeypatch):
    """Test initialization of ignore file."""
    monkeypatch.chdir(temp_repo)

    with patch("sys.argv", ["reposaurus", "init-ignore"]):
        main()

    ignore_file = temp_repo / ".reposaurusignore"
    assert ignore_file.exists()
    content = ignore_file.read_text()
    assert "# IDE and Version Control" in content
    assert ".git/" in content
    assert "# Build and Distribution" in content


def test_detect_idiots_command(temp_repo, monkeypatch, capsys):
    """Test secret detection functionality."""
    monkeypatch.chdir(temp_repo)

    secret_file = temp_repo / "secrets.py"
    secret_file.write_text('password = "super_secure_123"')

    with patch("sys.argv", ["reposaurus", "detect-idiots"]):
        main()

    captured = capsys.readouterr()
    output = captured.out
    assert any(word in output.lower() for word in ["password", "secret", "sensitive"])


def test_command_sequence(temp_repo, monkeypatch):
    """Test sequence of multiple commands working together."""
    monkeypatch.chdir(temp_repo)
    (temp_repo / "output").mkdir()

    # Write config file directly
    config = {
        "output": {
            "directory": "output",
            "filename_template": "test_output"
        }
    }
    with open(temp_repo / ".reposaurus.yml", "w") as f:
        yaml.dump(config, f)

    # Run fetch
    with patch("sys.argv", ["reposaurus", "fetch"]):
        main()

    assert any(Path(temp_repo / "output").glob("test_output*.txt"))


def test_error_handling(temp_repo, capsys):
    """Test CLI error handling scenarios."""
    with patch("sys.argv", ["reposaurus", "fetch", "/nonexistent/path"]):
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error" in captured.err or "Error" in captured.out


def test_versioning_behavior(temp_repo, monkeypatch):
    """Test output file versioning behavior."""
    monkeypatch.chdir(temp_repo)

    # Create output directory and config
    (temp_repo / "output").mkdir()
    config = {
        "output": {
            "directory": "output",
            "filename_template": "test_output",
            "versioning": {"enabled": True, "format": "numeric"}
        }
    }
    with open(temp_repo / ".reposaurus.yml", "w") as f:
        yaml.dump(config, f)

    # Run fetch command thrice
    for _ in range(3):
        with patch("sys.argv", ["reposaurus", "fetch"]):
            main()

    # Check for versioned files
    outputs = list(Path(temp_repo / "output").glob("test_output*.txt"))
    assert len(outputs) > 0


def test_output_formatting(temp_repo, monkeypatch):
    """Test output file formatting and structure."""
    monkeypatch.chdir(temp_repo)

    config = {
        "output": {
            "directory": ".",
            "filename_template": "test_format"
        }
    }
    with open(temp_repo / ".reposaurus.yml", "w") as f:
        yaml.dump(config, f)

    with patch("sys.argv", ["reposaurus", "fetch"]):
        main()

    output_files = list(temp_repo.glob("test_format*.txt"))
    assert len(output_files) > 0
    content = output_files[0].read_text()

    assert "# Repository Information" in content
    assert "Name:" in content
    assert "Absolute Path:" in content