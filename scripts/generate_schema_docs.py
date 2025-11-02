#!/usr/bin/env python3
"""
Generate comprehensive schema documentation for all endpoints.

This script generates RST documentation files for each endpoint schema,
including:
- Schema overview
- Method listings with parameters
- Example code for each functional method
- Deep dive into schema JSON
"""

from pathlib import Path

from pymlb_statsapi import api
from pymlb_statsapi.model.registry import EXCLUDED_METHODS


def get_functional_methods(endpoint_name: str) -> tuple[list[str], list[str]]:
    """
    Get lists of functional and non-functional methods for an endpoint.

    Returns:
        Tuple of (functional_methods, non_functional_methods)
    """
    endpoint = api.get_endpoint(endpoint_name)
    # get_method_names() already excludes non-functional methods
    functional = endpoint.get_method_names()
    # Get excluded methods from the registry
    non_functional = list(EXCLUDED_METHODS.get(endpoint_name, set()))

    return functional, non_functional


def generate_method_example(endpoint_name: str, method_name: str) -> str:
    """Generate a Python code example for a method."""
    try:
        info = api.get_method_info(endpoint_name, method_name)
        params = info.get("query_params", []) + info.get("path_params", [])

        # Build example parameters
        example_params = []
        for param in params[:3]:  # Limit to 3 params for brevity
            param_name = param["name"]
            param_type = param.get("type", "string")

            # Generate example values based on type
            if param_type == "integer":
                example_val = "1"
            elif param_name in ["date", "startDate", "endDate"]:
                example_val = '"2024-07-04"'
            elif param_name in ["season"]:
                example_val = '"2024"'
            elif param_name.endswith("Id"):
                example_val = "147"
            else:
                example_val = '"value"'

            example_params.append(f"{param_name}={example_val}")

        params_str = ", ".join(example_params) if example_params else ""

        code = f"""from pymlb_statsapi import api

# {info.get("summary", "API call")}
response = api.{endpoint_name.capitalize()}.{method_name}({params_str})
data = response.json()

# Save to file
result = response.save_json(prefix="mlb-data")
print(f"Saved to: {{result['path']}}")"""

        return code
    except Exception as e:
        return f"# Error generating example: {e}"


def generate_endpoint_doc(endpoint_name: str, output_dir: Path):
    """Generate RST documentation for a single endpoint."""
    functional_methods, non_functional_methods = get_functional_methods(endpoint_name)

    # Start building RST content
    title = f"{endpoint_name.capitalize()} Endpoint"
    lines = [
        title,
        "=" * len(title),
        "",
        f"The ``{endpoint_name}`` endpoint provides access to {endpoint_name}-related data from the MLB Stats API.",
        "",
        ".. contents:: Table of Contents",
        "   :local:",
        "   :depth: 2",
        "",
    ]

    # Overview section
    lines.extend(
        [
            "Overview",
            "-" * 50,
            "",
            f"This endpoint has **{len(functional_methods)} functional methods** and "
            f"**{len(non_functional_methods)} non-functional methods**.",
            "",
        ]
    )

    # Functional methods section
    if functional_methods:
        lines.extend(
            [
                "Functional Methods",
                "-" * 50,
                "",
                "The following methods are fully functional and tested:",
                "",
            ]
        )

        for method_name in sorted(functional_methods):
            try:
                info = api.get_method_info(endpoint_name, method_name)
                lines.extend(
                    [
                        f"{method_name}()",
                        "^" * (len(method_name) + 2),
                        "",
                        f"**Summary:** {info.get('summary', 'N/A')}",
                        "",
                        f"**Path:** ``{info.get('path', 'N/A')}``",
                        "",
                    ]
                )

                # Parameters
                path_params = info.get("path_params", [])
                query_params = info.get("query_params", [])

                if path_params:
                    lines.append("**Path Parameters:**")
                    lines.append("")
                    for param in path_params:
                        req = "**required**" if param.get("required") else "*optional*"
                        lines.append(
                            f"- ``{param['name']}`` (*{param.get('type', 'string')}*, {req}): {param.get('description', 'N/A')}"
                        )
                    lines.append("")

                if query_params:
                    lines.append("**Query Parameters:**")
                    lines.append("")
                    for param in query_params[:5]:  # Show first 5
                        req = "**required**" if param.get("required") else "*optional*"
                        lines.append(
                            f"- ``{param['name']}`` (*{param.get('type', 'string')}*, {req}): {param.get('description', 'N/A')}"
                        )
                    if len(query_params) > 5:
                        lines.append(f"- ... and {len(query_params) - 5} more parameters")
                    lines.append("")

                # Example
                lines.extend(
                    [
                        "**Example:**",
                        "",
                        ".. code-block:: python",
                        "",
                    ]
                )
                example = generate_method_example(endpoint_name, method_name)
                for line in example.split("\n"):
                    lines.append(f"   {line}")
                lines.extend(["", ""])

            except Exception as e:
                lines.extend(
                    [
                        f"*Error generating documentation: {e}*",
                        "",
                    ]
                )

    # Non-functional methods section
    if non_functional_methods:
        lines.extend(
            [
                "",
                "Non-Functional Methods",
                "-" * 50,
                "",
                ".. warning::",
                "",
                "   The following methods are **not functional** due to issues in the MLB Stats API or schema mismatches:",
                "",
            ]
        )

        for method_name in sorted(non_functional_methods):
            lines.append(f"   - ``{method_name}()``")

        lines.extend(
            [
                "",
                "   These methods are excluded from the API and will not be available.",
                "",
            ]
        )

    # Schema introspection section
    lines.extend(
        [
            "",
            "Schema Introspection",
            "-" * 50,
            "",
            f"You can explore the full schema for the ``{endpoint_name}`` endpoint programmatically:",
            "",
            ".. code-block:: python",
            "",
            "   from pymlb_statsapi import api",
            "",
            "   # List all methods",
            f"   methods = api.{endpoint_name.capitalize()}.get_method_names()",
            "   print(methods)",
            "",
            "   # Get method details",
            f"   method = api.{endpoint_name.capitalize()}.get_method('{'schedule' if endpoint_name == 'schedule' else functional_methods[0] if functional_methods else 'method_name'}')",
            "   schema = method.get_schema()",
            "   print(json.dumps(schema, indent=2))",
            "",
            "   # Get detailed description",
            f"   description = api.{endpoint_name.capitalize()}.describe_method('{'schedule' if endpoint_name == 'schedule' else functional_methods[0] if functional_methods else 'method_name'}')",
            "   print(description)",
            "",
        ]
    )

    # Write to file
    output_file = output_dir / f"{endpoint_name}.rst"
    output_file.write_text("\n".join(lines))
    print(f"Generated: {output_file}")


def generate_index_doc(endpoint_names: list[str], output_dir: Path):
    """Generate the schemas index page."""
    lines = [
        "Schema Reference",
        "=" * 50,
        "",
        "This section provides comprehensive documentation for all MLB Stats API endpoints.",
        "",
        ".. note::",
        "",
        "   These schemas were sourced from the MLB Stats API Beta documentation",
        "   (https://beta-statsapi.mlb.com/docs/), which is no longer publicly available.",
        "",
        "Each endpoint page includes:",
        "",
        "- Overview of functional and non-functional methods",
        "- Detailed parameter documentation",
        "- Python code examples",
        "- Schema introspection examples",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "   :caption: Endpoints",
        "",
    ]

    for name in sorted(endpoint_names):
        lines.append(f"   {name}")

    lines.extend(
        [
            "",
            "Quick Reference",
            "-" * 50,
            "",
            ".. code-block:: python",
            "",
            "   from pymlb_statsapi import api",
            "",
            "   # List all available endpoints",
            "   endpoints = api.get_endpoint_names()",
            "   print(endpoints)",
            "",
            "   # Get methods for an endpoint",
            "   methods = api.Schedule.get_method_names()",
            "   print(methods)",
            "",
            "   # Get detailed info about a method",
            "   info = api.get_method_info('schedule', 'schedule')",
            "   print(info)",
            "",
        ]
    )

    output_file = output_dir / "index.rst"
    output_file.write_text("\n".join(lines))
    print(f"Generated: {output_file}")


def main():
    """Main entry point."""
    # Create output directory
    docs_dir = Path(__file__).parent.parent / "docs"
    schemas_dir = docs_dir / "schemas"
    schemas_dir.mkdir(exist_ok=True)

    print("Generating schema documentation...")
    print("=" * 70)

    # Get all endpoints
    endpoint_names = api.get_endpoint_names()
    print(f"Found {len(endpoint_names)} endpoints")
    print()

    # Generate docs for each endpoint
    for endpoint_name in sorted(endpoint_names):
        try:
            generate_endpoint_doc(endpoint_name, schemas_dir)
        except Exception as e:
            print(f"Error generating docs for {endpoint_name}: {e}")

    # Generate index
    generate_index_doc(endpoint_names, schemas_dir)

    print()
    print("=" * 70)
    print(f"Generated documentation in: {schemas_dir}")
    print()
    print("Next steps:")
    print("1. Add schemas/index to docs/index.rst toctree")
    print("2. Run 'make docs' to build the documentation")
    print("3. Run 'make serve-docs' to view locally")


if __name__ == "__main__":
    main()
