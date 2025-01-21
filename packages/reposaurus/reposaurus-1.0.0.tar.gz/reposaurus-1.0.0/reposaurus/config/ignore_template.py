"""Default template for Reposaurus ignore file."""

IGNORE_TEMPLATE = """\
# Reposaurus Ignore File
# This file uses .gitignore syntax to specify which files should be excluded
# from the repository snapshot.

# Development Directories
.git/
.svn/
.vs/
.idea/
.vscode/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env/
.venv/
.pytest_cache/
.coverage
htmlcov/

# Build and Dependencies
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
*.egg
node_modules/
bower_components/
package-lock.json

# IDE and Editor Files
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Logs and Databases
*.log
*.sqlite
*.db

# Media and Binary Files
*.jpg
*.jpeg
*.png
*.gif
*.ico
*.pdf
*.zip
*.tar
*.gz
*.rar
*.7z
*.mp3
*.mp4
*.avi
*.mov

# Reposaurus Output Files
*_repository_contents*.txt
repository_contents.txt

# Project Specific
# Add your custom exclusions below
"""