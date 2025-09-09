#!/usr/bin/env python3
"""
Script to bump the version number in the project.
Usage: python scripts/bump_version.py <new_version>
Example: python scripts/bump_version.py 1.0.2
"""

import sys
import re
import os
from pathlib import Path


def update_version_file(new_version: str) -> None:
    """Update the version in opentargets_validator/version.py"""
    version_file = Path("opentargets_validator/version.py")
    
    if not version_file.exists():
        print(f"Error: {version_file} not found")
        sys.exit(1)
    
    content = version_file.read_text()
    
    # Replace the version line
    pattern = r'__version__ = "[^"]*"'
    replacement = f'__version__ = "{new_version}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content == content:
        print(f"Warning: Version line not found or already set to {new_version}")
    else:
        version_file.write_text(new_content)
        print(f"Updated version to {new_version} in {version_file}")


def update_pyproject_toml(new_version: str) -> None:
    """Update the version in pyproject.toml if it exists"""
    pyproject_file = Path("pyproject.toml")
    
    if not pyproject_file.exists():
        print("pyproject.toml not found, skipping")
        return
    
    content = pyproject_file.read_text()
    
    # Look for version = "..." line
    pattern = r'version = "[^"]*"'
    replacement = f'version = "{new_version}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        pyproject_file.write_text(new_content)
        print(f"Updated version to {new_version} in {pyproject_file}")
    else:
        print("pyproject.toml uses dynamic versioning, no update needed")


def validate_version(version: str) -> bool:
    """Validate that the version follows semantic versioning"""
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py <new_version>")
        print("Example: python scripts/bump_version.py 1.0.2")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    if not validate_version(new_version):
        print(f"Error: Invalid version format '{new_version}'")
        print("Version must follow semantic versioning (e.g., 1.0.2)")
        sys.exit(1)
    
    print(f"Bumping version to {new_version}...")
    
    # Change to the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    update_version_file(new_version)
    update_pyproject_toml(new_version)
    
    print(f"Version successfully bumped to {new_version}")
    print("\nNext steps:")
    print(f"1. git add opentargets_validator/version.py")
    print(f"2. git commit -m 'Bump version to {new_version}'")
    print(f"3. git tag v{new_version}")
    print(f"4. git push origin main")
    print(f"5. git push origin v{new_version}")


if __name__ == "__main__":
    main()
