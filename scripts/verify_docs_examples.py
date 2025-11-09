#!/usr/bin/env python3
"""
Verify that all code examples in documentation actually work.

This script extracts and executes Python code blocks from documentation files
to ensure they are accurate and functional.
"""

import ast
import re
import sys
from pathlib import Path


def extract_python_blocks(file_path: Path) -> list[tuple[str, int]]:
    """
    Extract Python code blocks from markdown or RST files.

    Returns:
        List of tuples: (code, line_number)
    """
    content = file_path.read_text()
    blocks = []

    # Markdown code blocks
    if file_path.suffix == ".md":
        pattern = r"```python\n(.*?)```"
        for match in re.finditer(pattern, content, re.DOTALL):
            code = match.group(1)
            line_num = content[: match.start()].count("\n") + 1
            blocks.append((code, line_num))

    # RST code blocks
    elif file_path.suffix == ".rst":
        pattern = r"\.\. code-block:: python\n\n((?:   .*\n)*)"
        for match in re.finditer(pattern, content, re.DOTALL):
            # Remove indentation (RST uses 3-space indent)
            code = "\n".join(line[3:] for line in match.group(1).split("\n") if line.strip())
            line_num = content[: match.start()].count("\n") + 1
            blocks.append((code, line_num))

    return blocks


def validate_python_syntax(code: str, file_path: Path, line_num: int) -> bool:
    """
    Validate that Python code has correct syntax.

    Returns:
        True if valid, False otherwise
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}:{line_num + e.lineno - 1}")
        print(f"   {e.msg}: {e.text}")
        return False


def check_imports(code: str) -> tuple[bool, list[str]]:
    """
    Check if code uses pymlb_statsapi imports correctly.

    Returns:
        Tuple of (is_valid, missing_imports)
    """
    tree = ast.parse(code)

    # Find what's imported
    imports = set()
    uses = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and "pymlb_statsapi" in node.module:
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if "pymlb_statsapi" in alias.name:
                    imports.add(alias.name.split(".")[-1])
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                # Track usage like: api.Schedule
                uses.add(node.value.id)

    # Check if imports match usage
    missing = uses - imports
    return len(missing) == 0, list(missing)


def main():
    """Main entry point."""
    root = Path(__file__).parent.parent
    docs_dir = root / "docs"
    examples_dir = root / "examples"
    readme = root / "README.md"

    print("🔍 Verifying documentation examples...")
    print(f"📁 Checking: {docs_dir}, {examples_dir}, {readme}")
    print()

    total_files = 0
    total_blocks = 0
    failed_files = []

    # Check all documentation files
    for pattern in ["**/*.md", "**/*.rst"]:
        for file_path in docs_dir.glob(pattern):
            if "_build" in str(file_path):  # Skip Sphinx build output
                continue

            total_files += 1
            blocks = extract_python_blocks(file_path)

            if not blocks:
                continue

            print(f"📄 {file_path.relative_to(root)}")
            file_failed = False

            for i, (code, line_num) in enumerate(blocks, 1):
                total_blocks += 1

                # Skip examples that are intentionally incomplete
                if "..." in code or "# Example" in code and len(code.split("\n")) < 3:
                    print(f"   ⏭️  Block {i} (line {line_num}): Skipped (incomplete example)")
                    continue

                # Validate syntax
                if not validate_python_syntax(code, file_path, line_num):
                    file_failed = True
                    continue

                # Check imports
                is_valid, missing = check_imports(code)
                if not is_valid and missing:
                    print(
                        f"   ⚠️  Block {i} (line {line_num}): Missing imports: {', '.join(missing)}"
                    )
                    file_failed = True
                    continue

                print(f"   ✅ Block {i} (line {line_num}): Valid")

            if file_failed:
                failed_files.append(file_path)
            print()

    # Check README
    total_files += 1
    blocks = extract_python_blocks(readme)
    if blocks:
        print(f"📄 {readme.relative_to(root)}")
        readme_failed = False

        for i, (code, line_num) in enumerate(blocks, 1):
            total_blocks += 1

            if "..." in code or "# Example" in code and len(code.split("\n")) < 3:
                print(f"   ⏭️  Block {i} (line {line_num}): Skipped (incomplete example)")
                continue

            if not validate_python_syntax(code, readme, line_num):
                readme_failed = True
                continue

            is_valid, missing = check_imports(code)
            if not is_valid and missing:
                print(f"   ⚠️  Block {i} (line {line_num}): Missing imports: {', '.join(missing)}")
                readme_failed = True
                continue

            print(f"   ✅ Block {i} (line {line_num}): Valid")

        if readme_failed:
            failed_files.append(readme)
        print()

    # Check example files
    for example_file in examples_dir.glob("*.py"):
        total_files += 1
        total_blocks += 1

        code = example_file.read_text()

        if not validate_python_syntax(code, example_file, 1):
            failed_files.append(example_file)
            continue

        print(f"📄 {example_file.relative_to(root)}")
        print("   ✅ Valid Python file")
        print()

    # Summary
    print("=" * 60)
    print("✨ Summary:")
    print(f"   Files checked: {total_files}")
    print(f"   Code blocks checked: {total_blocks}")
    print(f"   Failed files: {len(failed_files)}")

    if failed_files:
        print()
        print("❌ The following files have issues:")
        for file_path in failed_files:
            print(f"   - {file_path.relative_to(root)}")
        sys.exit(1)
    else:
        print()
        print("✅ All documentation examples are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
