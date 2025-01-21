"""
Reposaurus - Repository to Text Converter
A powerful tool for transforming repositories into comprehensive text files.
"""

__version__ = "0.1.7"
__author__ = "Andy Thomas"
__email__ = "your.email@example.com"

from pathlib import Path

# Package base directory
PACKAGE_DIR = Path(__file__).parent

# Make key components available at package level
from .cli.main import main  # noqa