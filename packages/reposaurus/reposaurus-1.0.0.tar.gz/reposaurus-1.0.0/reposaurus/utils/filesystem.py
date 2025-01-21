"""File system utility functions."""

import os
from pathlib import Path
from typing import Optional, Union
import chardet


def is_binary_file(file_path: Union[str, Path], sample_size: int = 8192) -> bool:
    """
    Check if a file is binary by reading its first bytes.

    Args:
        file_path: Path to the file to check
        sample_size: Number of bytes to check (default: 8KB)

    Returns:
        True if the file appears to be binary
    """
    try:
        with open(file_path, 'rb') as f:
            sample = f.read(sample_size)
            if not sample:  # Empty files are considered text
                return False

            # Check for null bytes
            if b'\x00' in sample:
                return True

            # Try to decode as text
            try:
                sample.decode('utf-8')
                return False
            except UnicodeDecodeError:
                return True

    except Exception:
        return True  # Assume binary if we can't read the file


def detect_encoding(file_path: Union[str, Path]) -> str:
    """
    Detect the encoding of a text file.

    Args:
        file_path: Path to the file

    Returns:
        Detected encoding or 'utf-8' as fallback
    """
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
            if not raw:
                return 'utf-8'
            result = chardet.detect(raw)
            return result['encoding'] or 'utf-8'
    except Exception:
        return 'utf-8'


def safe_read_file(file_path: Union[str, Path]) -> Optional[str]:
    """
    Safely read a text file with encoding detection.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents as string or None if file cannot be read
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']

    try:
        if is_binary_file(file_path):
            return None

        # First try chardet
        detected_encoding = detect_encoding(file_path)
        if detected_encoding:
            encodings.insert(0, detected_encoding)

        # Try each encoding
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {str(e)}")
                return None

        print(f"Warning: Could not determine encoding for {file_path}")
        return None
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {str(e)}")
        return None


def ensure_directory(path: Union[str, Path]) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    Path(path).mkdir(parents=True, exist_ok=True)