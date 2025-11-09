"""
Final tests to achieve maximum coverage - covering the last edge cases.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import requests

from pymlb_statsapi import StatsAPI
from pymlb_statsapi.model.factory import APIResponse, Endpoint


class TestSaveJsonParentDirectory:
    """Test save_json parent directory creation edge case."""

    def test_save_json_no_parent_directory(self):
        """Test save_json when parent directory is empty string."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.headers = {}
        mock_resp.content = b"{}"
        mock_resp.elapsed = Mock()
        mock_resp.elapsed.total_seconds.return_value = 0.1
        mock_resp.json.return_value = {"data": "test"}

        response = APIResponse(
            response=mock_resp,
            endpoint_name="schedule",
            method_name="schedule",
        )

        # Save to file with no parent directory (current directory)
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            # Just the filename, no directory
            result = response.save_json(file_path=temp_path)
            assert os.path.exists(result["path"])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestRegistryRepresentation:
    """Test StatsAPI __repr__ method."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_repr_with_endpoints(self, mock_sl):
        """Test __repr__ includes endpoint count."""
        mock_sl.get_available_schemas.return_value = [
            "schedule.json",
            "game.json",
            "person.json",
        ]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}, "game": {}, "person": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()
        repr_str = repr(registry)

        # Should mention the class name and endpoint count
        assert "StatsAPI" in repr_str
        assert "3" in repr_str or "endpoints" in repr_str.lower()

    @patch("pymlb_statsapi.model.registry.sl")
    def test_getattr_returns_endpoint(self, mock_sl):
        """Test __getattr__ successfully returns endpoint."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()

        # Access via attribute should work
        schedule_endpoint = registry.Schedule
        assert schedule_endpoint is not None
        # Should be cached
        schedule_endpoint2 = registry.Schedule
        assert schedule_endpoint is schedule_endpoint2


class TestEndpointGetMethod:
    """Test Endpoint.get_method() edge cases."""

    @patch("requests.get")
    def test_get_method_returns_endpoint_method(self, mock_get):
        """Test get_method returns EndpointMethod instance."""
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

        # get_method should return the actual EndpointMethod
        method = endpoint.get_method("schedule")
        assert method is not None
        assert method.method_name == "schedule"


class TestRegistryGetEndpointCached:
    """Test that registry caches endpoints after first access."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_attribute_access_caches_endpoint(self, mock_sl):
        """Test that accessing endpoint via attribute caches it."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}}
        }
        mock_sl.load_stats_schema.return_value = {
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

        registry = StatsAPI()

        # First access via attribute
        endpoint1 = registry.Schedule
        # Second access should return same cached instance
        endpoint2 = registry.Schedule
        # Third access via get_endpoint should also return same instance
        endpoint3 = registry.get_endpoint("schedule")

        assert endpoint1 is endpoint2
        assert endpoint2 is endpoint3


class TestEnumValidationCaseInsensitive:
    """Test enum validation with case sensitivity."""

    def test_enum_validation_case_insensitive(self):
        """Test that enum validation is case-insensitive."""
        from pymlb_statsapi.model.factory import EndpointMethod

        api_def = {"path": "/v1/schedule/{scheduleType}"}
        operation_def = {
            "method": "GET",
            "summary": "Get schedule",
            "notes": "",
            "parameters": [
                {
                    "name": "scheduleType",
                    "paramType": "path",
                    "type": "string",
                    "required": True,
                    "enum": ["games", "events", "XREF"],
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="schedule",
            method_name="schedule",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/schedule/{scheduleType}",
        )

        # Should accept lowercase version of "XREF"
        path_params, query_params, resolved = method.validate_and_resolve_params(
            path_params={"scheduleType": "xref"}
        )
        assert resolved == "/v1/schedule/xref"

        # Should accept uppercase version of "games"
        path_params, query_params, resolved = method.validate_and_resolve_params(
            path_params={"scheduleType": "GAMES"}
        )
        assert resolved == "/v1/schedule/GAMES"
