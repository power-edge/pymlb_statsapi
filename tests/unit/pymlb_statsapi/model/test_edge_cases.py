"""
Unit tests for edge cases and uncovered lines in factory.py and registry.py.
"""

from unittest.mock import Mock, patch

import pytest
import requests

from pymlb_statsapi import StatsAPI
from pymlb_statsapi.model.factory import APIResponse, Endpoint, EndpointMethod


class TestAPIResponseProperties:
    """Test APIResponse property accessors."""

    @pytest.fixture
    def api_response(self):
        """Create a mock APIResponse for testing."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.text = "Response text content"
        mock_resp.content = b"Response byte content"
        mock_resp.headers = {"Content-Type": "application/json", "X-Custom": "value"}
        mock_resp.json.return_value = {"data": "test"}
        mock_resp.elapsed = Mock()
        mock_resp.elapsed.total_seconds.return_value = 0.5

        return APIResponse(
            response=mock_resp,
            endpoint_name="schedule",
            method_name="schedule",
        )

    def test_text_property(self, api_response):
        """Test text property returns response text."""
        assert api_response.text == "Response text content"

    def test_content_property(self, api_response):
        """Test content property returns response bytes."""
        assert api_response.content == b"Response byte content"

    def test_headers_property(self, api_response):
        """Test headers property returns dict of headers."""
        headers = api_response.headers
        assert isinstance(headers, dict)
        assert headers["Content-Type"] == "application/json"
        assert headers["X-Custom"] == "value"


class TestEndpointMethodLongDescription:
    """Test get_long_description with all edge cases."""

    def test_long_description_with_enum_params(self):
        """Test get_long_description includes enum values."""
        api_def = {"path": "/v1/schedule/{scheduleType}"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "Returns schedule data",
            "parameters": [
                {
                    "name": "scheduleType",
                    "paramType": "path",
                    "type": "string",
                    "required": True,
                    "description": "Type of schedule",
                    "enum": ["games", "events", "xref"],
                },
                {
                    "name": "sportId",
                    "paramType": "query",
                    "type": "integer",
                    "required": False,
                    "description": "Sport ID",
                    "enum": [1, 2, 3],
                },
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule/{scheduleType}",
        )

        description = method.get_long_description()

        # Check enum values are included
        assert "Allowed values: games, events, xref" in description
        assert "Allowed values: 1, 2, 3" in description

    def test_long_description_with_allow_multiple(self):
        """Test get_long_description includes allowMultiple flag."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [
                {
                    "name": "teamId",
                    "paramType": "query",
                    "type": "array",
                    "required": False,
                    "description": "Team IDs",
                    "allowMultiple": True,
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        description = method.get_long_description()

        # Check allowMultiple is documented
        assert "Allows multiple values (comma-separated)" in description

    def test_long_description_with_response_messages(self):
        """Test get_long_description includes response codes."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [],
            "responseMessages": [
                {"code": 200, "message": "Success"},
                {"code": 404, "message": "Not found"},
                {"code": 500, "message": "Server error"},
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        description = method.get_long_description()

        # Check response codes are documented
        assert "Response Codes:" in description
        assert "200: Success" in description
        assert "404: Not found" in description
        assert "500: Server error" in description


class TestParameterValidationEdgeCases:
    """Test parameter validation edge cases."""

    def test_path_param_list_with_multiple_values_error(self):
        """Test that path params with multiple values raise error."""
        api_def = {"path": "/v1/game/{game_pk}"}
        operation_def = {
            "method": "GET",
            "summary": "Get game",
            "notes": "",
            "parameters": [
                {
                    "name": "game_pk",
                    "paramType": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="game",
            method_name="game",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/game/{game_pk}",
        )

        # Path param as list with multiple values should error
        with pytest.raises(
            AssertionError, match="path parameter 'game_pk' must have exactly one value"
        ):
            method.validate_and_resolve_params(path_params={"game_pk": [123, 456]})

    def test_path_param_list_with_single_value(self):
        """Test that path params with single-item list work."""
        api_def = {"path": "/v1/game/{game_pk}"}
        operation_def = {
            "method": "GET",
            "summary": "Get game",
            "notes": "",
            "parameters": [
                {
                    "name": "game_pk",
                    "paramType": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="game",
            method_name="game",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/game/{game_pk}",
        )

        # Path param as list with single value should extract the value
        validated_path, validated_query, resolved = method.validate_and_resolve_params(
            path_params={"game_pk": [123]}
        )

        assert validated_path["game_pk"] == "123"
        assert resolved == "/v1/game/123"

    def test_unrecognized_path_params_error(self):
        """Test that unrecognized path params raise error."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        # Unrecognized path params should error
        with pytest.raises(AssertionError, match="unrecognized path parameters: \\['invalid'\\]"):
            method.validate_and_resolve_params(path_params={"invalid": "value"})

    def test_required_query_param_missing_error(self):
        """Test that missing required query params raise error."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [
                {
                    "name": "sportId",
                    "paramType": "query",
                    "type": "integer",
                    "required": True,
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        # Missing required query param should error
        with pytest.raises(AssertionError, match="query parameter 'sportId' is required"):
            method.validate_and_resolve_params(query_params={})

    def test_query_param_multiple_values_not_allowed_error(self):
        """Test that multiple values for non-allowMultiple query params raise error."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [
                {
                    "name": "sportId",
                    "paramType": "query",
                    "type": "integer",
                    "required": False,
                    "allowMultiple": False,
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        # Multiple values when not allowed should error
        with pytest.raises(
            AssertionError, match="query parameter 'sportId' does not allow multiple values"
        ):
            method.validate_and_resolve_params(query_params={"sportId": [1, 2]})

    def test_unrecognized_query_params_error(self):
        """Test that unrecognized query params raise error."""
        api_def = {"path": "/v1/schedule"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule",
        )

        # Unrecognized query params should error
        with pytest.raises(AssertionError, match="unrecognized query parameters: \\['invalid'\\]"):
            method.validate_and_resolve_params(query_params={"invalid": "value"})


class TestEndpointMethodInfo:
    """Test endpoint method info retrieval."""

    @patch("requests.get")
    def test_get_method_info(self, mock_get):
        """Test get_method_info returns dict with method details."""
        from datetime import timedelta

        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_response.json.return_value = {"dates": []}
        mock_response.headers = {}
        mock_response.content = b"{}"
        mock_response.elapsed = timedelta(milliseconds=100)
        mock_get.return_value = mock_response

        schema = {
            "apis": [
                {
                    "path": "/v1/schedule",
                    "description": "schedule",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "schedule",
                            "summary": "Get schedule",
                            "notes": "Returns schedule data",
                            "parameters": [],
                        }
                    ],
                }
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={"schedule": {"path": "/v1/schedule"}},
        )

        # Get method info
        method_info = endpoint.get_method_info("schedule")

        assert isinstance(method_info, dict)
        assert method_info["name"] == "schedule"
        assert method_info["summary"] == "Get schedule"
        assert method_info["path"] == "/v1/schedule"
        assert method_info["http_method"] == "GET"

    @patch("requests.get")
    def test_get_method_info_not_found(self, mock_get):
        """Test get_method_info raises error for non-existent method."""
        schema = {
            "apis": [
                {
                    "path": "/v1/schedule",
                    "description": "schedule",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "schedule",
                            "summary": "Get schedule",
                            "notes": "",
                            "parameters": [],
                        }
                    ],
                }
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={"schedule": {"path": "/v1/schedule"}},
        )

        # Non-existent method should raise ValueError
        with pytest.raises(ValueError, match="Method 'nonexistent' not found"):
            endpoint.get_method_info("nonexistent")

    @patch("requests.get")
    def test_get_method_not_found(self, mock_get):
        """Test get_method raises error for non-existent method."""
        schema = {
            "apis": [
                {
                    "path": "/v1/schedule",
                    "description": "schedule",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "schedule",
                            "summary": "Get schedule",
                            "notes": "",
                            "parameters": [],
                        }
                    ],
                }
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={"schedule": {"path": "/v1/schedule"}},
        )

        # Non-existent method should raise ValueError with helpful message
        with pytest.raises(ValueError, match="Method 'nonexistent' not found on schedule endpoint"):
            endpoint.get_method("nonexistent")


class TestRegistryEdgeCases:
    """Test StatsAPI registry edge cases."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_getattr_not_found(self, mock_sl):
        """Test __getattr__ raises AttributeError for non-endpoint attributes."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()

        # Non-existent attribute should raise AttributeError
        with pytest.raises(
            AttributeError, match="'StatsAPI' object has no attribute 'NonExistent'"
        ):
            _ = registry.NonExistent

    @patch("pymlb_statsapi.model.registry.sl")
    def test_repr(self, mock_sl):
        """Test __repr__ returns string representation."""
        mock_sl.get_available_schemas.return_value = ["schedule.json", "game.json"]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}, "game": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()
        repr_str = repr(registry)

        assert "StatsAPI" in repr_str
        assert "endpoints" in repr_str.lower()
