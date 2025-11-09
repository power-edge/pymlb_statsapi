"""
Tests to achieve complete 100% coverage - covering the last remaining lines.
"""

from unittest.mock import Mock, patch

import requests

from pymlb_statsapi import StatsAPI
from pymlb_statsapi.model.factory import Endpoint
from pymlb_statsapi.model.registry import create_stats_api


class TestFormatParamsDoc:
    """Test _format_params_doc method."""

    @patch("requests.get")
    def test_format_params_doc_with_empty_params(self, mock_get):
        """Test _format_params_doc with empty parameter list."""
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
                            "parameters": [],  # Empty parameters
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

        # Call method to generate docstring (which calls _format_params_doc)
        # The docstring should include "None" for empty params
        method = endpoint.schedule
        assert method.__doc__ is not None


class TestDescribeMethod:
    """Test describe_method wrapper."""

    @patch("requests.get")
    def test_describe_method(self, mock_get):
        """Test describe_method calls get_long_description."""
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
                            "parameters": [
                                {
                                    "name": "sportId",
                                    "paramType": "query",
                                    "type": "integer",
                                    "required": False,
                                    "description": "Sport ID filter",
                                }
                            ],
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

        # Call describe_method
        description = endpoint.describe_method("schedule")

        # Should return long description
        assert isinstance(description, str)
        assert "schedule" in description.lower()
        assert "Get schedule" in description


class TestGetMethodSchema:
    """Test get_method_schema wrapper."""

    @patch("requests.get")
    def test_get_method_schema(self, mock_get):
        """Test get_method_schema calls get_schema."""
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

        # Call get_method_schema
        method_schema = endpoint.get_method_schema("schedule")

        # Should return schema dict
        assert isinstance(method_schema, dict)
        assert "operation" in method_schema
        assert "endpoint" in method_schema
        assert method_schema["endpoint"] == "schedule"


class TestRegistryGetAllMethods:
    """Test get_all_methods in registry."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_get_all_methods(self, mock_sl):
        """Test get_all_methods returns mapping of endpoints to methods."""
        mock_sl.get_available_schemas.return_value = ["schedule.json", "game.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}},
            "game": {"game": {"path": "/v1/game/{game_pk}"}},
        }

        # Return schemas with operations
        def mock_load_stats_schema(name):
            if name == "schedule":
                return {
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
            elif name == "game":
                return {
                    "apis": [
                        {
                            "path": "/v1/game/{game_pk}",
                            "description": "game",
                            "operations": [
                                {
                                    "method": "GET",
                                    "nickname": "game",
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
                            ],
                        }
                    ]
                }

        mock_sl.load_stats_schema.side_effect = mock_load_stats_schema

        registry = StatsAPI()
        all_methods = registry.list_all_methods()

        # Should return dict mapping endpoints to method lists
        assert isinstance(all_methods, dict)
        assert "schedule" in all_methods
        assert "game" in all_methods
        assert "schedule" in all_methods["schedule"]
        assert "game" in all_methods["game"]


class TestRegistryGetMethodInfo:
    """Test get_method_info in registry."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_get_method_info(self, mock_sl):
        """Test get_method_info returns method details."""
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
        method_info = registry.get_method_info("schedule", "schedule")

        # Should return dict with method details
        assert isinstance(method_info, dict)
        assert method_info["name"] == "schedule"
        assert method_info["path"] == "/v1/schedule"


class TestCreateStatsAPI:
    """Test create_stats_api factory function."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_create_stats_api_function(self, mock_sl):
        """Test create_stats_api factory function."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        # Create using factory function
        new_api = create_stats_api()

        assert isinstance(new_api, StatsAPI)
        assert "schedule" in new_api.get_endpoint_names()

    @patch("pymlb_statsapi.model.registry.sl")
    def test_create_stats_api_with_exclusions(self, mock_sl):
        """Test create_stats_api with custom exclusions."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {"schedule": {}}
        mock_sl.load_stats_schema.return_value = {"apis": []}

        # Create with exclusions
        exclusions = {"schedule": {"some_method"}}
        new_api = create_stats_api(excluded_methods=exclusions)

        assert isinstance(new_api, StatsAPI)
