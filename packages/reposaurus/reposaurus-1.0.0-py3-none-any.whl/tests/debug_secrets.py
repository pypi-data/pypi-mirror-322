"""Debug script to check file content."""


def debug_file():
    with open('tests/fixtures/secrets/test_secrets.py', 'r') as f:
        content = f.read()
    print("Raw content with escapes:")
    print(repr(content))

    print("\nActual newlines:")
    for i, line in enumerate(content.splitlines(), 1):
        if "BEGIN" in line or "END" in line:
            print(f"Line {i}: {repr(line)}")


if __name__ == "__main__":
    debug_file()