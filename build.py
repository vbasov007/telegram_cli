#!/usr/bin/env python3
"""
Build script for creating telegram_send.exe using PyInstaller.
This can be run from any platform but is optimized for Windows.
"""
import subprocess
import sys
import os
from pathlib import Path


def check_venv():
    """Check if running in a virtual environment."""
    if not hasattr(sys, 'prefix') or sys.prefix == sys.base_prefix:
        print("Warning: Not running in a virtual environment.")
        print("Consider activating .venv before running this script.")
        return False
    return True


def install_pyinstaller():
    """Install PyInstaller from requirements-dev.txt."""
    print("Installing PyInstaller...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
            check=True
        )
        print("PyInstaller installed successfully.\n")
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install PyInstaller")
        return False


def build_executable(use_spec=False):
    """Build the executable using PyInstaller."""
    print("Building executable...")

    try:
        if use_spec:
            print("Using spec file for build...")
            subprocess.run(
                [sys.executable, "-m", "PyInstaller", "telegram_send.spec"],
                check=True
            )
        else:
            print("Using command-line options for build...")
            subprocess.run([
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name", "telegram_send",
                "--console",
                "telegram_send.py"
            ], check=True)

        print("\n" + "="*50)
        print("Build completed successfully!")
        print("="*50)
        print(f"\nThe executable is located at: {Path('dist/telegram_send.exe').absolute()}")
        print("\nIMPORTANT: Remember to create telegram_send_config.ini in the same directory as the .exe")
        return True
    except subprocess.CalledProcessError:
        print("Error: Build failed")
        return False


def main():
    """Main build function."""
    print("="*50)
    print("Building telegram_send.exe")
    print("="*50)
    print()

    # Check if in virtual environment
    check_venv()

    # Install PyInstaller
    if not install_pyinstaller():
        sys.exit(1)

    # Determine which build method to use
    use_spec = '--spec' in sys.argv or os.path.exists('telegram_send.spec')

    # Build the executable
    if not build_executable(use_spec):
        sys.exit(1)

    print("\nBuild process completed!")


if __name__ == '__main__':
    main()
