"""Central pattern management for Reposaurus."""

# File and directory patterns that should be excluded from processing
DEFAULT_EXCLUDE_PATTERNS = [
    # Development Directories
    ".git/",
    ".svn/",
    ".vs/",
    ".idea/",
    ".vscode/",
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "env/",
    "venv/",
    ".env/",
    ".venv/",
    ".pytest_cache/",
    ".coverage",
    "htmlcov/",

    # Build and Dependencies
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "*.egg-info/",
    "*.egg",
    "node_modules/",
    "bower_components/",
    "package-lock.json",

    # IDE and Editor Files
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "Thumbs.db",

    # Logs and Databases
    "*.log",
    "*.sqlite",
    "*.db",

    # Media and Binary Files
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.gif",
    "*.ico",
    "*.pdf",
    "*.zip",
    "*.tar",
    "*.gz",
    "*.rar",
    "*.7z",
    "*.mp3",
    "*.mp4",
    "*.avi",
    "*.mov",

    # Reposaurus Output Files
    "*_repository_contents*.txt",
    "repository_contents.txt",
]

# Patterns for detecting sensitive information
# Order matters - more specific patterns should come before general ones
SECRET_PATTERNS = {
    # Specific key types first (with negative lookahead to prevent double-matching)
    'github_token': r'(?i)(gh[ops]_[A-Za-z0-9_]*|github[_-]token)["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',
    'aws_key': r'(?i)(aws[_-](?:key|secret|token))["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',
    'crypto_key': r'(?i)(crypto[_-]key|encryption[_-]key)["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',

    # Certificate and key files - match content directly
    'private_key': r'-----BEGIN\s+(?:RSA\s+)?PRIVATE KEY-----[\s\S]*?-----END\s+(?:RSA\s+)?PRIVATE KEY-----',
    'certificate': r'-----BEGIN\s+CERTIFICATE-----[\s\S]*?-----END\s+CERTIFICATE-----',
    'ssh_key': r'(?i)ssh-rsa\s+AAAA[0-9A-Za-z+/]+[=]{0,3}',

    # Connection strings with potential credentials
    'connection_string': r'(?i)(mongodb(\+srv)?://|postgres://|mysql://|redis://|jdbc:)[^\s"\']+:[^\s"\']+@[^\s"\']+',

    # General API and authentication tokens
    'api_key': r'(?i)(?<!test_)(?<!aws_)(api[_-]key|apikey|api\s+key)["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',
    'token': r'(?i)(?<!test_)(?<!github_)(?<!gh[ops]_)(token|auth[_-]token|access[_-]token)["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',
    'secret': r'(?i)(?<!test_)(?<!aws_)(secret|app[_-]secret)["\s]*[:=]\s*[\'"]([\w\-]+)[\'"]',

    # Passwords (both variable assignment and dictionary/JSON style)
    'password': r'(?i)(?<!test_)(password|passwd|pwd)[\s"\']*[:=]\s*[\'"]([\w\-@#$%^&*!]+)[\'"]',
}

# Default allowlist for known safe matches
DEFAULT_ALLOWLIST = {
    # Documentation examples
    "README.md": [],
    "tests/fixtures/secrets/test_secrets.py": [],

    # Configuration templates
    "reposaurus/config/config_template.py": [
        'API_KEY = "DEMO_KEY_FOR_TESTING"',
        'API_KEY = "DEFINITELY_NOT_REAL"',
        'PASSWORD = "EXAMPLE_PASSWORD_NOT_REAL"'
    ],

    # Core templates and patterns
    "reposaurus/core/secrets.py": [
        '-----BEGIN CERTIFICATE-----',
        '-----BEGIN (?!EXAMPLE )CERTIFICATE-----'
    ],

    # Test directories and fixtures
    "tests/": [
        'TEST_API_KEY = "TEST_KEY"',
        'TEST_PASSWORD = "TEST_PASSWORD"',
        'TOKEN = "TEST_TOKEN"'
    ],

    "tests/fixtures/secrets/": [
        'TEST_API_KEY = "TEST_KEY"',
        'TEST_PASSWORD = "TEST_PASSWORD"'
    ]

}

# Default configuration template
DEFAULT_CONFIG = {
    'patterns': {
        'use_default_ignores': True,
        'ignore_file_path': '.reposaurusignore',
        'additional_excludes': []
    },
    'output': {
        'filename_template': '{repo_name}_repository_contents',
        'directory': '.',
        'versioning': {
            'enabled': True,
            'format': 'numeric',
            'start_fresh': False
        },
        'section_separator': 'line',
        'separator_length': 48
    },
    'git': {
        'auto_update_gitignore': True
    },
    'detect_secrets': {
        'patterns': {},  # Additional patterns beyond defaults
        'exclude_patterns': [],  # Patterns to exclude from detection
        'allowlist': {}  # Additional allowlist beyond defaults
    }
}