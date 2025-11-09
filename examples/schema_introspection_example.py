#!/usr/bin/env python3
"""
Example: Schema Introspection and Parameter Discovery

This example demonstrates how to access the original JSON schemas
and discover API parameters without reading external documentation.

The API preserves exact parameter names from the MLB Stats API (like sportId, not sport_id).
"""

import json

from pymlb_statsapi import api

print("=" * 70)
print("Schema Introspection Example")
print("=" * 70)
print()

# Example 1: Get full method description
print("Example 1: Get Full Method Description")
print("-" * 70)

# Get a human-readable description of the schedule method
description = api.Schedule.describe_method("schedule")
print(description)
print()

# Example 2: Access original schema JSON
print("\nExample 2: Access Original Schema JSON")
print("-" * 70)

# Get the full schema definition
method = api.Schedule.get_method("schedule")
schema = method.get_schema()

print(f"Endpoint: {schema['endpoint']}")
print(f"Method: {schema['method']}")
print(f"Path: {schema['api']['path']}")
print(f"Description: {schema['api']['description']}")
print()

# Example 3: List all parameters
print("\nExample 3: List All Parameters")
print("-" * 70)

params = method.list_parameters()

print("Path Parameters:")
for param in params["path"]:
    print(f"  - {param['name']} ({param['type']})")
    print(f"    Required: {param['required']}")
    print(f"    {param['description']}")
print()

print("Query Parameters:")
for param in params["query"][:5]:  # Show first 5 to keep output manageable
    print(f"  - {param['name']} ({param['type']})")
    print(f"    Required: {param['required']}")
    print(f"    {param['description']}")
print(f"... and {len(params['query']) - 5} more query parameters")
print()

# Example 4: Get specific parameter details
print("\nExample 4: Get Specific Parameter Details")
print("-" * 70)

# Get details for the sportId parameter (note: exact name preserved!)
param_schema = method.get_parameter_schema("sportId")
if param_schema:
    print(f"Parameter: {param_schema['name']}")
    print(f"Type: {param_schema.get('type', 'string')}")
    print(f"Required: {param_schema.get('required', False)}")
    print(f"Description: {param_schema.get('description', 'N/A')}")
    print(f"Format: {param_schema.get('format', 'N/A')}")

    # Check if it has enum values
    if "enum" in param_schema and param_schema["enum"]:
        print(f"Allowed values: {', '.join(str(v) for v in param_schema['enum'])}")
print()

# Example 5: Discover methods on an endpoint
print("\nExample 5: Discover Methods on an Endpoint")
print("-" * 70)

print("Available methods on Schedule endpoint:")
for method_name in api.Schedule.get_method_names():
    method = api.Schedule.get_method(method_name)
    print(f"  - {method_name}()")
    print(f"    Path: {method.path_template}")
    print(f"    Summary: {method.summary}")
print()

# Example 6: Check parameter names are preserved (camelCase, not snake_case)
print("\nExample 6: Parameter Names Are Preserved")
print("-" * 70)

# The MLB Stats API uses camelCase for parameters
# Our library preserves these exact names (NOT converted to snake_case)

print("✓ Parameters preserve original names from MLB Stats API:")
print("  - sportId (NOT sport_id)")
print("  - teamId (NOT team_id)")
print("  - gamePk (NOT game_pk)")
print()

# You can use them exactly as documented in the MLB Stats API:
print("Example usage with preserved parameter names:")
print("  api.Schedule.schedule(sportId=1, date='2025-06-01')")
print("  api.Team.team(teamId='147', season='2024')")
print("  api.Game.liveGameV1(game_pk='747175')  # Note: game_pk uses underscore in schema")
print()

# Example 7: Get schema for a method with path parameters
print("\nExample 7: Method with Path Parameters")
print("-" * 70)

game_method = api.Game.get_method("liveGameV1")
print(game_method.get_long_description())
print()

# Example 8: Use schema info to build requests programmatically
print("\nExample 8: Build Requests Programmatically")
print("-" * 70)

# Get all required parameters
params = api.Schedule.get_method("schedule").list_parameters()
required_path = [p for p in params["path"] if p["required"]]
required_query = [p for p in params["query"] if p["required"]]

print(f"Required path parameters: {[p['name'] for p in required_path] or 'None'}")
print(f"Required query parameters: {[p['name'] for p in required_query] or 'None'}")
print()

# Build a valid request
print("Building a request with optional parameters:")
optional_params = [p["name"] for p in params["query"][:3]]
print(f"Using parameters: {', '.join(optional_params)}")
print()

# Example 9: Export schema to JSON for external tools
print("\nExample 9: Export Schema to JSON")
print("-" * 70)

schema = api.Schedule.get_method_schema("schedule")

# Save to file for external tools
schema_json = json.dumps(schema, indent=2)
print("Schema can be exported to JSON for external tools:")
print(f"Total schema size: {len(schema_json)} characters")
print("Contains: API definition, operation details, all parameters")
print()

# Show a snippet
print("Schema snippet:")
print(
    json.dumps(
        {
            "endpoint": schema["endpoint"],
            "method": schema["method"],
            "path": schema["api"]["path"],
            "http_method": schema["operation"]["method"],
            "parameter_count": len(schema["operation"].get("parameters", [])),
        },
        indent=2,
    )
)
print()

print("=" * 70)
print("Schema introspection allows you to:")
print("  1. Discover available parameters without external docs")
print("  2. Access original MLB Stats API schema definitions")
print("  3. Build requests programmatically")
print("  4. Export schemas for external tools")
print("  5. Debug API issues with full parameter details")
print("=" * 70)
