"""
Step definitions for StatsAPI testing with stub support.
"""

import json
import os
from unittest.mock import Mock

import requests
from behave import given, then, when

from pymlb_statsapi import api
from pymlb_statsapi.model.factory import APIResponse


@given("I use the {endpoint_name} endpoint")
def step_use_endpoint(context, endpoint_name):
    """Select an endpoint to work with."""
    context.endpoint_name = endpoint_name
    context.endpoint = api.get_endpoint(endpoint_name)
    assert context.endpoint is not None, f"Endpoint '{endpoint_name}' not found"


@given("I call the {method_name} method")
def step_call_method(context, method_name):
    """Select a method to call."""
    context.method_name = method_name
    assert hasattr(context.endpoint, method_name), (
        f"Method '{method_name}' not found on {context.endpoint_name}"
    )
    context.method = getattr(context.endpoint, method_name)


@given("I use path parameters: {path_params}")
def step_use_path_params(context, path_params):
    """Set path parameters."""
    context.path_params = json.loads(path_params)


@given("I use query parameters: {query_params}")
def step_use_query_params(context, query_params):
    """Set query parameters."""
    context.query_params = json.loads(query_params)


@given("I use no path parameters")
def step_use_no_path_params(context):
    """Set empty path parameters."""
    context.path_params = {}


@given("I use no query parameters")
def step_use_no_query_params(context):
    """Set empty query parameters."""
    context.query_params = {}


@when("I make the API call")
def step_make_api_call(context):
    """
    Make the API call, using stubs if available.

    Behavior depends on stub mode (from tags or STUB_MODE env):
    - replay: Use stub if available, fail if not
    - capture: Make real call and save stub
    - passthrough: Make real call without saving
    """
    stub_mode = context.stub_mode
    path_params = getattr(context, "path_params", {})
    query_params = getattr(context, "query_params", {})

    # Merge path_params and query_params into a single kwargs dict for the new API
    # The method internally knows which params are path vs query based on schema
    all_params = {**path_params, **query_params}

    # Check if stub exists
    stub_data = context.stub_manager.load_stub(
        context.endpoint_name, context.method_name, path_params, query_params
    )

    if stub_mode == "replay":
        # Must use stub
        assert stub_data is not None, (
            f"Stub not found for {context.endpoint_name}.{context.method_name} "
            f"(path={path_params}, query={query_params}). "
            f"Run with STUB_MODE=capture to create it."
        )
        context.response = _create_response_from_stub(stub_data)
        context.stub_data = stub_data
        context.stats["stubs_replayed"] += 1
        resource_path = stub_data.get("path", stub_data.get("url", "unknown"))
        print(f"  → Replayed stub: {resource_path}")

    elif stub_mode == "capture":
        # Make real API call with clean parameter passing
        try:
            context.response = context.method(**all_params)
            context.stats["api_calls_made"] += 1

            # Save stub
            stub_path = context.stub_manager.capture_stub(context.response)
            context.captured_stubs.append(stub_path)
            context.stats["stubs_captured"] += 1
            print(f"  → Captured: {context.response.get_path()}")
        except Exception as e:
            context.error = e
            raise

    else:  # passthrough
        # Make real API call without saving, with clean parameter passing
        try:
            context.response = context.method(**all_params)
            context.stats["api_calls_made"] += 1
            print(f"  → Passthrough: {context.response.get_path()}")
        except Exception as e:
            context.error = e
            raise


@then("the response should be successful")
def step_response_successful(context):
    """Verify response was successful."""
    assert context.response is not None, "No response available"
    assert context.response.ok, f"Response failed with status {context.response.status_code}"
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"


@then("the response should contain the field {field}")
def step_response_contains_field(context, field):
    """Verify response contains a specific field."""
    data = context.response.json()
    assert field in data, f"Response missing field '{field}'. Available: {list(data.keys())}"


@then("the response should contain a list in {field}")
def step_response_contains_list(context, field):
    """Verify response contains a list in a specific field."""
    data = context.response.json()
    assert field in data, f"Response missing field '{field}'"
    assert isinstance(data[field], list), f"Field '{field}' is not a list"


@then("the response should not be empty")
def step_response_not_empty(context):
    """Verify response is not empty."""
    data = context.response.json()
    assert data, "Response is empty"


@then("the resource path should match the pattern {pattern}")
def step_resource_path_matches(context, pattern):
    """Verify resource path matches expected pattern."""
    path = context.response.get_path()
    assert pattern in path, f"Resource path '{path}' does not contain '{pattern}'"


@then("I can save the response to a file")
def step_save_response(context):
    """Verify we can save the response."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        result = context.response.save_json(f.name)
        assert result["path"] == f.name
        assert result["bytes_written"] > 0
        # Clean up
        os.remove(f.name)


@then("the {list_field} should have at least {min_count:d} items")
def step_list_min_count(context, list_field, min_count):
    """Verify a list field has minimum number of items."""
    data = context.response.json()
    assert list_field in data, f"Field '{list_field}' not found"
    items = data[list_field]
    assert isinstance(items, list), f"Field '{list_field}' is not a list"
    assert len(items) >= min_count, f"Expected at least {min_count} items, got {len(items)}"


@then("each item in {list_field} should have {required_field}")
def step_list_items_have_field(context, list_field, required_field):
    """Verify each item in a list has a required field."""
    data = context.response.json()
    items = data[list_field]
    for i, item in enumerate(items):
        assert required_field in item, f"Item {i} in '{list_field}' missing '{required_field}'"


def _create_response_from_stub(stub_data: dict) -> APIResponse:
    """Create an APIResponse object from stub data."""
    from datetime import timedelta

    # Create a mock requests.Response
    mock_response = Mock(spec=requests.Response)
    mock_response.url = stub_data["url"]
    mock_response.status_code = stub_data["status_code"]
    mock_response.ok = 200 <= stub_data["status_code"] < 300
    mock_response.text = json.dumps(stub_data["response"])
    mock_response.content = mock_response.text.encode()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = stub_data["response"]
    mock_response.elapsed = timedelta(milliseconds=0)  # Add elapsed time for get_metadata()

    # Create APIResponse
    return APIResponse(
        response=mock_response,
        endpoint_name=stub_data["endpoint"],
        method_name=stub_data["method"],
        path_params=stub_data["path_params"],
        query_params=stub_data["query_params"],
    )
