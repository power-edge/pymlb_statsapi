#!/usr/bin/env python3
"""
Validate Setup Script

Run this before pushing to verify everything is configured correctly.

Usage:
    python scripts/validate_setup.py
"""

import json
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_mark(passed: bool) -> str:
    return f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"


def print_header(text: str):
    print(f"\n{BLUE}{'=' * 70}")
    print(f"{text}")
    print(f"{'=' * 70}{RESET}\n")


def print_section(text: str):
    print(f"\n{YELLOW}{text}{RESET}")
    print("-" * 70)


def validate_sponsor_links() -> bool:
    """Check if sponsor links have been updated."""
    print_section("Checking Sponsor Links")

    issues = []

    # Check FUNDING.yml
    funding_file = Path(".github/FUNDING.yml")
    if funding_file.exists():
        content = funding_file.read_text()
        if "YOUR_KOFI_USERNAME" in content:
            issues.append("  - .github/FUNDING.yml still has placeholder 'YOUR_KOFI_USERNAME'")
        if "YOUR_GITHUB_USERNAME" in content:
            issues.append("  - .github/FUNDING.yml still has placeholder 'YOUR_GITHUB_USERNAME'")
        if "YOUR_PATREON_USERNAME" in content:
            issues.append("  - .github/FUNDING.yml still has placeholder 'YOUR_PATREON_USERNAME'")
        if "YOUR_USERNAME" in content:
            issues.append("  - .github/FUNDING.yml still has placeholder 'YOUR_USERNAME'")
    else:
        issues.append("  - .github/FUNDING.yml not found")

    # Check README.md
    readme_file = Path("README.md")
    if readme_file.exists():
        content = readme_file.read_text()
        if "YOUR_USERNAME" in content or "YOUR_KOFI_USERNAME" in content:
            issues.append("  - README.md still has sponsor link placeholders")
    else:
        issues.append("  - README.md not found")

    if issues:
        print(f"{check_mark(False)} Sponsor links need updating:")
        for issue in issues:
            print(issue)
        return False
    else:
        print(f"{check_mark(True)} Sponsor links are configured")
        return True


def validate_documentation_files() -> bool:
    """Check if required documentation files exist."""
    print_section("Checking Documentation Files")

    required_files = [
        "docs/conf.py",
        "docs/index.rst",
        ".readthedocs.yml",
        "README.md",
        "CLEAN_API_REFACTOR.md",
        "SCHEMA_INTROSPECTION.md",
    ]

    optional_docs = [
        "docs/installation.rst",
        "docs/quickstart.rst",
        "docs/usage.rst",
        "docs/testing.rst",
        "docs/contributing.rst",
        "docs/architecture.rst",
        "docs/changelog.rst",
        "docs/license.rst",
    ]

    missing_required = []
    missing_optional = []

    for file in required_files:
        if not Path(file).exists():
            missing_required.append(file)

    for file in optional_docs:
        if not Path(file).exists():
            missing_optional.append(file)

    if missing_required:
        print(f"{check_mark(False)} Missing required documentation files:")
        for file in missing_required:
            print(f"  - {file}")

    if missing_optional:
        print(f"{YELLOW}⚠{RESET}  Missing optional documentation files (needed for ReadTheDocs):")
        for file in missing_optional:
            print(f"  - {file}")
        print("\nRun the RST file creation commands from NEXT_STEPS.md to create these.")

    if not missing_required:
        print(f"{check_mark(True)} Required documentation files exist")

    return len(missing_required) == 0


def validate_configuration_files() -> bool:
    """Check if required configuration files exist."""
    print_section("Checking Configuration Files")

    required_configs = {
        ".github/workflows/ci-cd.yml": "GitHub Actions CI/CD",
        ".github/FUNDING.yml": "Sponsor links",
        ".readthedocs.yml": "ReadTheDocs config",
        "pyproject.toml": "Project configuration",
        "Makefile": "Build automation",
        ".pre-commit-config.yaml": "Pre-commit hooks",
    }

    all_exist = True
    for file, description in required_configs.items():
        exists = Path(file).exists()
        print(f"{check_mark(exists)} {description}: {file}")
        if not exists:
            all_exist = False

    return all_exist


def validate_code_structure() -> bool:
    """Check if key code files exist."""
    print_section("Checking Code Structure")

    key_files = [
        "pymlb_statsapi/model/factory.py",
        "pymlb_statsapi/model/registry.py",
        "pymlb_statsapi/utils/schema_loader.py",
        "features/steps/statsapi_steps.py",
        "examples/clean_api_demo.py",
        "examples/schema_introspection_example.py",
    ]

    all_exist = True
    for file in key_files:
        exists = Path(file).exists()
        print(f"{check_mark(exists)} {file}")
        if not exists:
            all_exist = False

    return all_exist


def validate_examples() -> bool:
    """Try to import and basic syntax check of examples."""
    print_section("Validating Examples")

    try:
        # Try basic import
        from pymlb_statsapi import api

        print(f"{check_mark(True)} Can import pymlb_statsapi.model.registry.api")

        # Check endpoint access
        schedule = api.Schedule
        print(
            f"{check_mark(True)} Can access api.Schedule endpoint: {json.dumps(schedule, default=str)}"
        )

        # Check method access
        method = api.Schedule.get_method("schedule")
        print(f"{check_mark(True)} Can get method metadata: {json.dumps(method, default=str)}")

        # Check schema access
        schema = method.get_schema()
        print(
            f"{check_mark(True)} Can access original schema JSON: {json.dump(schema, default=str)}"
        )

        return True
    except Exception as e:
        print(f"{check_mark(False)} Import/access error: {e}")
        return False


def check_git_status():
    """Check git status."""
    print_section("Checking Git Status")

    try:
        import subprocess  # nosec B404 - Safe: only used for git commands

        # Check if in git repo. nosec is for B603 & B607 which are excepted as we are using git with hardcoded args
        result = subprocess.run(  # nosec
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )

        if result.stdout.strip():
            print(f"{YELLOW}⚠{RESET}  You have uncommitted changes:")
            print(result.stdout)
            print("\nConsider committing before pushing.")
        else:
            print(f"{check_mark(True)} No uncommitted changes")

    except subprocess.CalledProcessError:
        print(f"{YELLOW}⚠{RESET}  Not in a git repository or git not available")
    except FileNotFoundError:
        print(f"{YELLOW}⚠{RESET}  Git not found in PATH")


def main():
    """Run all validation checks."""
    print_header("PyMLB StatsAPI Setup Validation")

    print("This script checks if your setup is ready for deployment.\n")

    results = {
        "Sponsor Links": validate_sponsor_links(),
        "Documentation Files": validate_documentation_files(),
        "Configuration Files": validate_configuration_files(),
        "Code Structure": validate_code_structure(),
        "Examples/Imports": validate_examples(),
    }

    check_git_status()

    # Summary
    print_header("Validation Summary")

    all_passed = all(results.values())

    for check, passed in results.items():
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"{status}  {check}")

    print()

    if all_passed:
        print(f"{GREEN}{'=' * 70}")
        print("✅ All validation checks passed!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Commit and push: git add . && git commit -m 'feat: ...' && git push")
        print("2. Set up Codecov: https://codecov.io/")
        print("3. Set up ReadTheDocs: https://readthedocs.org/")
        print(f"{'=' * 70}{RESET}")
        return 0
    else:
        print(f"{RED}{'=' * 70}")
        print("❌ Some validation checks failed")
        print("=" * 70)
        print("\nPlease fix the issues above before pushing.")
        print("See NEXT_STEPS.md for detailed guidance.")
        print(f"{'=' * 70}{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
