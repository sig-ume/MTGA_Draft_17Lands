#!/usr/bin/env python3
"""Development environment setup script.

Usage:
    python setup_dev.py
"""

import subprocess
import sys


def main():
    print("Installing development dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
        check=True,
    )

    print("Setting up pre-commit hooks...")
    subprocess.run(["pre-commit", "install"], check=True)

    print("Done! Development environment is ready.")


if __name__ == "__main__":
    main()
