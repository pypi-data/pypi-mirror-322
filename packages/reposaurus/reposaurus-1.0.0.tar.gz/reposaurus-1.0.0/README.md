![Reposaurus Banner](assets/reposaurus-banner.png)

# 🦕 Reposaurus

A command-line tool that transforms Git repositories into comprehensive, searchable text files. It intelligently processes your codebase by excluding binary files, development artifacts, and sensitive data, while preserving the repository structure and content. Perfect for AI model training, documentation generation, code review preparation, and project archiving. Simply specify a repository path and optional configuration, and it generates a clean, well-formatted snapshot of your codebase with built-in versioning support.

# Overview

Reposaurus is a high-performance tool that converts Git repositories into structured, searchable text files. It employs intelligent pattern matching and configuration systems to ensure you capture exactly what you need from your codebase, while automatically excluding irrelevant files and potential security risks.

Whether you're training AI models, conducting security audits, preparing for code reviews, or creating project documentation, Reposaurus streamlines the process of generating clean, consistent snapshots of your codebase.

## Core Features

### 📁 Repository Processing
- 🔄 Incremental Processing with Smart Caching
- 📊 Hierarchical Directory Structure Visualization
- 📝 Comprehensive File Content Extraction
- 🎯 Intelligent Binary File Detection
- 💻 Multi-encoding Support (UTF-8, ASCII, etc.)
- ⚡ Parallel Processing for Large Repositories

### 🛡️ Security & Compliance
- 🔐 Advanced Secret Detection
  - Pre-configured patterns for API keys, tokens, and credentials
  - Custom pattern matching for organization-specific secrets
  - Allowlist system for approved test credentials
  - Clear, actionable security reports
- 📋 Compliance Helpers
  - License detection and reporting
  - Third-party dependency tracking
  - Customizable compliance checks

### ⚙️ Configuration & Control
- 📝 YAML-based Configuration
  - Global and project-specific settings
  - Environment variable support
  - Inheritance and override capabilities
- 🎯 Advanced Pattern Matching
  - Simple glob patterns for common cases
  - Full gitignore syntax support
  - Custom regex patterns for precise control
- 📑 Flexible Output Options
  - Versioned output files
  - Custom naming patterns
  - Structured formats (Text, JSON, YAML)

### 📊 Analysis & Insights
- 📈 Repository Metrics
  - File and directory statistics
  - Language distribution
  - Code complexity indicators
- 🔍 Content Analysis
  - Token and symbol counting
  - Dependency graphs
  - Custom metric tracking
- 📱 Interactive CLI Dashboard
  - Real-time processing status
  - Progress indicators
  - Rich terminal output with --show-analysis flag

# Installation

Install Reposaurus using pip:

```bash
pip3 install reposaurus
```

## Development Installation

For development, install Reposaurus with additional development dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/reposaurus.git
cd reposaurus

# Install in editable mode with development dependencies
pip install -e .[dev]
```

On macOS, you might need to add Python's bin directory to your PATH:
```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

# Basic Usage

## Fetching a Repository as Text

The main command you'll use is `reposaurus fetch`. Here's everything it does by default:

### Default Output Location
- Creates files in your current working directory (or target repository directory)
- First run creates: `repository_contents.txt`
- Subsequent runs create versioned files using one of two formats:
  - Numeric: `repository_contents_v1.txt`, `repository_contents_v2.txt`, etc.
  - Date-based: `repository_contents_20250105_202514.txt` (if configured)
- You can customize the output location and naming in `.reposaurus.yml`
- Auto-detects existing versions and continues sequence

### Automatic Features
- Binary File Detection: Automatically identifies and skips binary files
- Encoding Detection: Smart detection of text file encodings (UTF-8, ASCII, etc.)
- Development Artifact Exclusion: Skips common directories like .git, node_modules
- .gitignore Integration: Automatically adds output files to your .gitignore
- Configuration Inheritance: Merges user config with smart defaults
- Permission Checking: Validates read/write access before processing
- Error Recovery: Continues processing even if individual files fail

### Output Format Structure
- Repository Header:
  ```
  ================================================
  # Repository Information
  ------------------------------------------------
  Repository Information:
  Name: project-name
  Absolute Path: /path/to/project
  Relative Path: /path/to/project

  Configuration Settings:
  Use Default Ignores: True
  Ignore File: .reposaurusignore
  Output Directory: .
  Versioning: numeric

  Generated: 2025-01-05 20:25:14
  ```
- Directory Structure (with proper indentation)
- File Contents:
  ```
  ================================================
  # File: path/to/file
  ------------------------------------------------
  [File contents here]
  ```

### What's Included By Default
- Repository metadata (name, path, timestamp)
- Complete directory structure in a tree format
- Full contents of all text files
- Section separators for easy navigation
- Clear file path headers

### File Exclusion Options

Reposaurus provides flexible ways to control which files are included in your repository snapshot:

#### 1. Command-Line Exclusions
Use the `--exclude` or `-x` flag to specify files or directories to exclude:
```bash
# Exclude specific files and directories
reposaurus fetch --exclude logs/,temp.txt,build/

# Multiple patterns are comma-separated
reposaurus fetch -x "*.log,node_modules/,dist/"
```

#### 2. Exclusion File
Use the `--exclude-file` or `-e` flag to specify a file containing exclusion patterns:
```bash
# Use a custom exclusion file
reposaurus fetch --exclude-file .repoexclude

# The exclusion file uses .gitignore syntax:
#   *.log       # Exclude all log files
#   build/      # Exclude build directory
#   temp.txt    # Exclude specific file
#   **/cache/   # Exclude cache directories at any depth
```

#### 3. Default Exclusions
Reposaurus automatically excludes common patterns:
- Version control directories (.git, .svn)
- Build artifacts and dependencies (node_modules, __pycache__)
- Binary files (detected automatically)
- Development files (.env, .vscode)

You can combine these approaches:
```bash
# Use both exclusion file and command-line patterns
reposaurus fetch -e .repoexclude -x "extra.log,temp/"
```

### Example Commands and Output
```bash
# Basic usage - process current directory
reposaurus fetch
→ Creates: ./repository_contents.txt or ./repository_contents_v1.txt

# Specify a different directory
reposaurus fetch /path/to/repo
→ Creates: /path/to/repo/repository_contents.txt

# Custom output location
reposaurus fetch --output ./docs/codebase.txt
→ Creates: ./docs/codebase.txt

# Show repository analysis metrics
reposaurus fetch --show-analysis
→ Displays file counts, lines of code, and file type distribution

# Exclude specific files and directories
reposaurus fetch --exclude "logs/,*.tmp,build/"
→ Excludes logs directory, .tmp files, and build directory

# Use a custom exclusion file
reposaurus fetch --exclude-file .repoexclude
→ Uses patterns from .repoexclude file

# Combine exclusion options
reposaurus fetch -e .repoexclude -x "extra.log,temp/"
→ Uses both file patterns and command-line exclusions

# Show analysis with custom output location
reposaurus fetch --show-analysis --output ./docs/codebase.txt
→ Creates file and shows metrics in terminal
```

Reposaurus offers several commands through its CLI:

```bash
# Process current directory with default settings
reposaurus fetch

# This creates repository_contents_v1.txt in your current directory
# Each subsequent run creates versioned files (v2, v3, etc.)
# The output includes full directory structure and all text file contents
# Binary files are automatically detected and skipped

# Process a specific directory
reposaurus fetch /path/to/repository

# Output analytics from the repository to the terminal
reposaurus fetch /path/to/repository --output custom_name.txt --show-analysis

# You can combine with other options
reposaurus fetch /path/to/repository --output custom_name.txt

# Use custom exclusion patterns
reposaurus fetch --exclude-file my_patterns.txt

# Create a default configuration file
reposaurus init-config

# Create a default ignore file
reposaurus init-ignore
```

## 🎯 The detect-idiots Command

Because we've all been there... This command helps you find secrets in your repository before someone else does!

```bash
# Find out who's been a bit too sharing with their secrets
reposaurus detect-idiots

# Check a specific directory of potential oopsies
reposaurus detect-idiots /path/to/repo

# Save the findings for a fun team meeting
reposaurus detect-idiots --output whoops.yml
```

### Output Format

The command will report findings in a clear, structured format:

```
Potential secrets found:
--------------------------------------------------
Type: [type of secret detected]
File: [file path]
Line: [line number]
Match: [matched text]
--------------------------------------------------
```

Common secret types detected include:
- API keys and tokens
- AWS credentials
- GitHub tokens
- Private keys and certificates
- Connection strings
- Passwords and secrets
- Crypto/encryption keys

### Why "detect-idiots"?

- Because "find-developers-who-need-a-hug" was too long
- Because we've all been that developer at least once
- Because naming things is hard, and humor helps the medicine go down

### What It Actually Does (Seriously Though)

- 🕵️‍♂️ Scans your repo for accidental secret commits
- 🔐 Finds API keys, tokens, and other sensitive data
- 🛡️ Helps protect your project before it becomes a security issue
- 🤫 Keeps your secrets secret (what a concept!)
- 🔎 Supports custom patterns for your specific "oops" scenarios

### The "Don't Be That Developer" Checklist

- ✔ Run detect-idiots before pushing to remote
- ✔ Use the allowlist for test credentials only
- ✔ Share the results privately with your team
- ✔ Fix issues before they become incidents
- ❌ Don't use it to find other people's secrets
- ❌ Don't commit secrets just to test if it works (yes, people do this)

### Customizing Your Secret Detection

```yaml
detect_secrets:
  patterns:
    custom_whoops: 'my_super_secret_pattern'
  allowlist:
    "test/config.js":
      - 'API_KEY = "DEMO_KEY_FOR_TESTING"'
```

Remember: This tool is for protecting developers from themselves, not for finding other people's mistakes. Use it responsibly, and maybe bring cookies to the team meeting where you discuss the findings. 🍪

### Ignoring Files and Directories

You can completely exclude specific files or directories from secret detection by adding them to the allowlist with an empty list:

```yaml
detect_secrets:
  allowlist:
    # Ignore a specific file
    tests/fixtures/secrets/test_secrets.py: []

    # Ignore all files in a directory
    tests/fixtures/secrets/: []

    # You can combine file exclusions with pattern allowlists
    tests/:
      - API_KEY = "TEST_KEY"    # Allow this pattern in all test files
    specs/test_secrets.py: []   # But completely ignore this specific file
```

Files specified with [] will be completely skipped during secret detection. This is useful for:

- Test files containing dummy secrets
- Example configuration files
- Documentation files with code samples
- Legacy files that have been reviewed

### A Note on Responsible Usage

This feature was created to help developers protect their code, not to exploit vulnerabilities. If you find secrets in a public repository:

1. 🤝 Contact the owner privately
2. ⌛ Give them time to fix it
3. 🔐 Don't use or share the secrets
4. 🤗 Be part of the solution
5. 🦕 Remember: Even dinosaurs kept their secrets safe

# Configuration

Reposaurus supports YAML configuration files for customizing behavior. Create a default configuration using:

```bash
reposaurus init-config
```

This creates a `.reposaurus.yml` file with the following options:

```yaml
patterns:
  # Use built-in default ignore patterns
  use_default_ignores: true

  # Path to custom ignore file
  ignore_file_path: ".reposaurusignore"

  # Additional patterns to always exclude
  additional_excludes:
    - ".git/"
    - ".idea/"
    - ".venv/"

output:
  # Template for output filename
  filename_template: "{repo_name}_repository_contents"

  # Output directory (relative to repository root)
  directory: "."

  # Version control for output files
  versioning:
    enabled: true
    format: "numeric"  # none, numeric, or date
    start_fresh: false

  # Section separator style
  section_separator: "line"
  separator_length: 48

git:
  # Automatically add output files to .gitignore
  auto_update_gitignore: true

detect_secrets:
  # Custom patterns to detect (in addition to defaults)
  patterns:
    custom_api_key: '(?i)my_api_key["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]'

  # Patterns to exclude from detection
  exclude_patterns:
    - "password"  # Excludes default password pattern

  # Allowlist of known safe matches
  allowlist:
    "config/settings.py":
      - 'API_KEY = "DEMO_KEY_FOR_TESTING"'
      - 'PASSWORD = "EXAMPLE_PASSWORD_NOT_REAL"'
```

## Pattern Matching System

Reposaurus employs a sophisticated dual approach to file exclusions:

### Default Pattern Matching

By default, Reposaurus automatically excludes common development artifacts:

- Development Directories:
  - Version control (`.git`, `.svn`)
  - IDE configurations (`.vs`, `.idea`, `.vscode`)
  - Python artifacts (`__pycache__`, `.egg-info`)
  - Virtual environments (`venv`, `.env`)

- Build and Dependencies:
  - Build outputs (`bin`, `obj`, `build`, `dist`)
  - Dependencies (`node_modules`, `packages`)
  - Cache directories (`.cache`, `__pycache__`)

- System and Binary Files:
  - System files (`.DS_Store`, `Thumbs.db`)
  - Compiled files (`.pyc`, `.exe`, `.dll`)
  - Archives (`.zip`, `.tar`, `.gz`)
  - Media files (`.jpg`, `.png`, `.mp3`)
  - Logs and databases (`.log`, `.sqlite`)

### Advanced Pattern Matching

For more control, create a custom `.reposaurusignore` file:

```bash
reposaurus init-ignore
```

This file supports full `.gitignore` syntax:

```gitignore
# Ignore all .txt files
*.txt

# But keep important.txt
!important.txt

# Ignore temp folders anywhere
**/temp/

# Ignore specific directories
build/
node_modules/

# Complex patterns
docs/**/*.md
!docs/README.md
```

## Command-Line Options

The `fetch` command supports several options:

```bash
reposaurus fetch [OPTIONS] [PATH]

Arguments:
  PATH                  Repository path (default: current directory)

Options:
  --output, -o         Output file path (default: repository_contents.txt)
  --exclude-file, -e   Path to custom exclusion file
  --exclude, -x        Comma-separated list of exclusion patterns
  --config, -c         Path to configuration file
  --show-analysis, -sa Display repository analysis metrics in terminal output
```

#### Analysis Metrics

When using the `--show-analysis` flag, Reposaurus displays:
- Total number of files in the repository
- Total lines of code
- Total token count (rough estimate of code complexity)
- Distribution of files by type (e.g., .py, .js, .md)

Example output:
```
Repository Analysis:
Total Files: 42
Total Lines: 1337
Total Tokens: 5280

Files by Type:
.py: 15
.js: 8
.md: 4
.yml: 2
.txt: 13
```

## Output Format and Versioning

The generated output file includes:

- Repository metadata and configuration settings
- Complete directory structure
- File contents with clear section separators

Versioning options include:
- `numeric`: Appends version numbers (e.g., `_v1`, `_v2`)
- `date`: Appends timestamps (e.g., `_20250105_202514`)
- `none`: No versioning

Example output structure:

```text
================================================
# Repository Information
------------------------------------------------
Repository Information:
Name: my-project
Absolute Path: /path/to/my-project
...

================================================
# Directory Structure
------------------------------------------------
    src/
    ├── main.py
    └── utils.py
    ...

================================================
# File: src/main.py
------------------------------------------------
[File contents here]
```

## Error Handling

Reposaurus includes robust error handling:
- Automatic binary file detection and skipping
- Intelligent file encoding detection
- Clear error messages for invalid patterns
- Graceful handling of permission issues
- Detailed warnings for processing problems
- Secure handling of detected sensitive information
- Configurable allowlists for false positives
- Clear reporting of potential security issues

## Contributing

We love contributions! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation
- Share how you're using Reposaurus

Before submitting a pull request, please ensure your code follows the project's style guidelines and includes appropriate tests.

## License

MIT License - See LICENSE file for details

## Authors

- Andy Thomas - Initial work