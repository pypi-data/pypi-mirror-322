#!/usr/bin/env python
"""
Release script for DataLib.
Usage: python scripts/release.py [major|minor|patch]
"""

import os
import re
import sys
from pathlib import Path

def update_version(version_type):
    """Update version based on semantic versioning."""
    # Read current version from __init__.py
    init_path = Path("src/datalib/__init__.py")
    with open(init_path) as f:
        content = f.read()
    
    # Extract current version
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find version string")
    
    current_version = match.group(1)
    major, minor, patch = map(int, current_version.split('.'))
    
    # Update version based on type
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ValueError("Version type must be major, minor, or patch")
    
    new_version = f"{major}.{minor}.{patch}"
    
    # Update __init__.py
    new_content = re.sub(
        r'__version__ = ["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )
    with open(init_path, "w") as f:
        f.write(new_content)
    
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path) as f:
        content = f.read()
    
    new_content = re.sub(
        r'version = ["\']([^"\']+)["\']',
        f'version = "{new_version}"',
        content
    )
    with open(pyproject_path, "w") as f:
        f.write(new_content)
    
    print(f"Updated version from {current_version} to {new_version}")
    return new_version

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Usage: python scripts/release.py [major|minor|patch]")
        sys.exit(1)
    
    version_type = sys.argv[1]
    try:
        new_version = update_version(version_type)
        print(f"""
Release {new_version} prepared. Next steps:
1. Review changes
2. Commit changes:
   git add src/datalib/__init__.py pyproject.toml
   git commit -m "Release version {new_version}"
   git tag v{new_version}
3. Build distribution:
   python -m build
4. Upload to PyPI:
   python -m twine upload dist/*
""")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 