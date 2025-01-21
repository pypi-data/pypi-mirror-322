# tests/test_helpers.py
import os
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Any
from contextlib import contextmanager

@pytest.fixture(scope="function")
def temp_test_dir(request) -> Generator[Path, None, None]:
    """
    Creates a unique temporary directory for each test function.
    The directory is automatically cleaned up after the test completes.
    """
    test_dir = Path(tempfile.mkdtemp(prefix=f"test_{request.node.name}_"))
    yield test_dir
    if test_dir.exists():
        shutil.rmtree(test_dir)

@pytest.fixture(scope="function")
def isolated_fs(temp_test_dir: Path) -> Generator[Path, None, None]:
    """
    Provides an isolated filesystem for tests by changing to a temporary directory
    and restoring the original directory after the test completes.
    """
    original_dir = os.getcwd()
    os.chdir(temp_test_dir)
    yield temp_test_dir
    os.chdir(original_dir)

@contextmanager
def temporary_file(content: str = "", suffix: str = "") -> Generator[Path, None, None]:
    """
    Creates a temporary file with optional content and suffix.
    The file is automatically cleaned up after use.
    """
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        if content:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        else:
            os.close(fd)
        yield Path(path)
    finally:
        if os.path.exists(path):
            os.unlink(path)

@pytest.fixture(scope="function")
def mock_repo_dir(temp_test_dir: Path) -> Generator[Path, None, None]:
    """
    Creates a mock repository directory structure for testing.
    """
    repo_dir = temp_test_dir / "mock_repo"
    repo_dir.mkdir(parents=True)
    (repo_dir / ".git").mkdir()
    yield repo_dir

@pytest.fixture(scope="function")
def clean_environment() -> Generator[None, None, None]:
    """
    Provides a clean environment by temporarily clearing specific environment variables
    that might affect test execution.
    """
    saved_environ = dict(os.environ)
    test_vars = ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_CONFIG']
    
    for var in test_vars:
        os.environ.pop(var, None)
    
    yield
    
    os.environ.clear()
    os.environ.update(saved_environ)

def unique_string_generator() -> Generator[str, None, None]:
    """
    Generates unique strings for test resources.
    """
    counter = 0
    while True:
        yield f"test_resource_{counter}"
        counter += 1

@pytest.fixture(scope="session")
def unique_string() -> Generator[Any, None, None]:
    """
    Provides unique strings for test resources throughout the test session.
    """
    generator = unique_string_generator()
    yield generator

# tests/conftest.py
import pytest

pytest_plugins = [
    "tests.test_helpers",
]

def pytest_configure(config):
    """
    Configure pytest for parallel execution.
    """
    config.addinivalue_line(
        "markers",
        "serial: mark test to run in serial (not parallel with other tests)"
    )

def pytest_collection_modifyitems(config, items):
    """
    Add serial marker to tests that cannot run in parallel.
    """
    for item in items:
        if "serial" in item.keywords:
            item.add_marker(pytest.mark.serial)