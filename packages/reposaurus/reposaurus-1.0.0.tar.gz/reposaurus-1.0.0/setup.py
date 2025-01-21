from setuptools import setup, find_packages
import codecs

# Read long description with proper encoding
with codecs.open("README.md", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name="reposaurus",
    version="1.0.0",  # Updated for new feature
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'reposaurus=reposaurus.cli.main:main',
        ],
    },
    install_requires=[
        'pathspec>=0.9.0',  # For gitignore-style pattern matching
        'chardet>=5.0.0',   # For file encoding detection
        'pyyaml>=6.0.1',    # For configuration and output handling
    ],
    extras_require={
        'dev': [
            'pytest>=7.3.1',
            'pytest-cov>=4.1.0',
            'pytest-xdist>=3.3.1',
            'pytest-mock>=3.11.1',
            'hypothesis>=6.86.2',
            'tox>=4.8.0',
            'black>=23.7.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.4.1',
            'pre-commit>=3.3.3',
            'twine>=4.0.0',
            'build>=1.0.0',
        ],
    },
    author="Andy Thomas",
    author_email="your.email@example.com",
    description="A powerful tool for transforming repositories into text files and detecting sensitive information innit...🦖",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reposaurus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Security",
    ],
    python_requires=">=3.7",  # Updated to match tox configuration
    test_suite='tests',
)