#!/usr/bin/env python3
"""Fix JSON syntax errors in stub files."""

import json
import sys
from pathlib import Path


def fix_json_file(filepath: Path) -> bool:
    """
    Fix JSON syntax by loading and re-saving.

    Returns True if fixed successfully, False if failed.
    """
    try:
        # Try to load the file
        with open(filepath) as f:
            data = json.load(f)

        # If successful, write it back cleanly
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return True
    except json.JSONDecodeError as e:
        print(f"❌ Cannot auto-fix {filepath.name}: {e.msg} at line {e.lineno}")
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath.name}: {e}")
        return False


def main():
    """Find and fix all JSON stub files."""
    root = Path(__file__).parent.parent
    stub_dir = root / "tests" / "bdd" / "stubs"

    if not stub_dir.exists():
        print(f"Stub directory not found: {stub_dir}")
        sys.exit(1)

    print(f"🔍 Scanning for JSON files in {stub_dir}")

    json_files = list(stub_dir.rglob("*.json"))
    print(f"📁 Found {len(json_files)} JSON files")

    fixed = 0
    failed = 0

    for json_file in json_files:
        if fix_json_file(json_file):
            fixed += 1
        else:
            failed += 1

    print()
    print(f"✅ Fixed: {fixed}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
        sys.exit(1)
    else:
        print("🎉 All JSON files are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
