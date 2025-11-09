"""
Unit tests for the dynamic API system.
"""

from unittest.mock import Mock, patch

import pytest
import requests

from pymlb_statsapi import StatsAPI, api
from pymlb_statsapi.model.factory import (
    APIResponse,
    Endpoint,
    EndpointMethod,
)


class TestAPIResponse:
    """Test APIResponse wrapper."""

    def test_init(self):
        """Test APIResponse initialization."""
        mock_response = Mock(spec=requests.Response)
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-07-04"
        mock_response.status_code = 200
        mock_response.ok = True

        response = APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
            path_params={},
            query_params={"sportId": "1", "date": "2024-07-04"},
        )

        assert response.endpoint_name == "schedule"
        assert response.method_name == "schedule"
        assert response.status_code == 200
        assert response.ok is True
        assert response.domain == "statsapi.mlb.com"
        assert response.path == "/api/v1/schedule"

    def test_json_removes_copyright(self):
        """Test that copyright is removed from JSON response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_response.json.return_value = {
            "copyright": "Copyright 2024 MLB Advanced Media",
            "dates": [{"date": "2024-07-04"}],
        }

        response = APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
        )

        data = response.json()
        assert "copyright" not in data
        assert "dates" in data

    def test_get_metadata(self):
        """Test get_metadata returns all request and response metadata."""
        from datetime import timedelta

        mock_response = Mock(spec=requests.Response)
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-07-04"
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.headers = {"Content-Type": "application/json", "Content-Length": "1234"}
        mock_response.content = b'{"test": "data"}'
        mock_response.elapsed = timedelta(milliseconds=245.3)

        response = APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
            path_params={},
            query_params={"sportId": "1", "date": "2024-07-04"},
        )

        metadata = response.get_metadata()

        # Check request metadata
        assert metadata["request"]["endpoint_name"] == "schedule"
        assert metadata["request"]["method_name"] == "schedule"
        assert metadata["request"]["path_params"] == {}
        assert metadata["request"]["query_params"] == {"sportId": "1", "date": "2024-07-04"}
        assert (
            metadata["request"]["url"]
            == "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-07-04"
        )
        assert metadata["request"]["scheme"] == "https"
        assert metadata["request"]["domain"] == "statsapi.mlb.com"
        assert metadata["request"]["path"] == "/api/v1/schedule"
        assert metadata["request"]["http_method"] == "GET"
        assert "timestamp" in metadata["request"]

        # Check response metadata
        assert metadata["response"]["status_code"] == 200
        assert metadata["response"]["ok"] is True
        assert abs(metadata["response"]["elapsed_ms"] - 245.3) < 0.01  # Floating point comparison
        assert metadata["response"]["content_type"] == "application/json"
        assert metadata["response"]["content_length"] == 16
        assert "Content-Type" in metadata["response"]["headers"]

    def test_to_dict_with_data(self):
        """Test to_dict returns metadata and data."""
        mock_response = Mock(spec=requests.Response)
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"dates": []}'
        mock_response.elapsed = Mock()
        mock_response.elapsed.total_seconds.return_value = 0.245
        mock_response.json.return_value = {"dates": [{"date": "2024-07-04"}]}

        response = APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
            path_params={},
            query_params={"sportId": "1"},
        )

        result = response.to_dict()

        # Check structure
        assert "metadata" in result
        assert "data" in result

        # Check metadata is complete
        assert "request" in result["metadata"]
        assert "response" in result["metadata"]

        # Check data is the parsed JSON
        assert result["data"] == {"dates": [{"date": "2024-07-04"}]}

    def test_to_dict_without_data(self):
        """Test to_dict with include_data=False returns only metadata."""
        mock_response = Mock(spec=requests.Response)
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule"
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"dates": []}'
        mock_response.elapsed = Mock()
        mock_response.elapsed.total_seconds.return_value = 0.245

        response = APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
        )

        result = response.to_dict(include_data=False)

        # Check structure
        assert "metadata" in result
        assert "data" not in result

        # Metadata should still be complete
        assert "request" in result["metadata"]
        assert "response" in result["metadata"]


class TestEndpointMethod:
    """Test EndpointMethod class."""

    def test_parameter_validation_required_missing(self):
        """Test that missing required parameters raise errors."""
        api_def = {"path": "/v1/game/{game_pk}/boxscore"}
        operation_def = {
            "method": "GET",
            "summary": "Get boxscore",
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
            method_name="boxscore",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/game/{game_pk}/boxscore",
        )

        with pytest.raises(AssertionError, match="path parameter 'game_pk' is required"):
            method.validate_and_resolve_params(path_params={})

    def test_parameter_validation_enum(self):
        """Test enum validation."""
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
                    "enum": ["games", "events", "xref"],
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

        # Valid enum value
        path_params, query_params, resolved = method.validate_and_resolve_params(
            path_params={"scheduleType": "games"}
        )
        assert resolved == "/v1/schedule/games"

        # Invalid enum value
        with pytest.raises(AssertionError, match="must be one of"):
            method.validate_and_resolve_params(path_params={"scheduleType": "invalid"})

    def test_query_param_multiple_values(self):
        """Test query parameters with multiple values."""
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

        path_params, query_params, resolved = method.validate_and_resolve_params(
            query_params={"teamId": [147, 111]}
        )

        assert query_params["teamId"] == "147,111"


@patch("requests.get")
class TestDynamicEndpoint:
    """Test DynamicEndpoint class."""

    def test_method_generation(self, mock_get):
        """Test that methods are dynamically generated."""
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
                    ],
                }
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={"schedule": {"path": "/v1/schedule"}},
        )

        # Check method was created
        assert hasattr(endpoint, "schedule")
        assert "schedule" in endpoint.get_method_names()

    def test_method_exclusion(self, mock_get):
        """Test that excluded methods are not generated."""
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
                },
                {
                    "path": "/v1/schedule/broken",
                    "description": "brokenMethod",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "brokenMethod",
                            "summary": "Broken endpoint",
                            "notes": "",
                            "parameters": [],
                        }
                    ],
                },
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={},
            excluded_methods={"brokenMethod"},
        )

        assert hasattr(endpoint, "schedule")
        assert not hasattr(endpoint, "brokenMethod")
        assert "schedule" in endpoint.get_method_names()
        assert "brokenMethod" not in endpoint.get_method_names()

    def test_request_execution(self, mock_get):
        """Test that requests are executed correctly."""
        from datetime import timedelta

        # Setup mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
        mock_response.json.return_value = {"dates": []}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"dates": []}'
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
                    ],
                }
            ]
        }

        endpoint = Endpoint(
            endpoint_name="schedule",
            schema=schema,
            endpoint_config={"schedule": {"path": "/v1/schedule"}},
        )

        # Call the method - parameters are passed directly as kwargs
        response = endpoint.schedule(sportId=1)

        # Verify request was made
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "https://statsapi.mlb.com/api/v1/schedule?sportId=1" in call_args[0]

        # Verify response
        assert isinstance(response, APIResponse)
        assert response.status_code == 200


class TestDynamicStatsAPI:
    """Test DynamicStatsAPI registry."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_initialization(self, mock_sl):
        """Test that registry initializes with endpoints."""
        mock_sl.get_available_schemas.return_value = ["schedule.json", "game.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}},
            "game": {},
        }
        mock_sl.load_stats_schema.side_effect = [
            {"apis": []},  # schedule schema
            {"apis": []},  # game schema
        ]

        assert "schedule" in api.get_endpoint_names()
        assert "game" in api.get_endpoint_names()
        assert hasattr(api, "Schedule")
        assert hasattr(api, "Game")

    @patch("pymlb_statsapi.model.registry.sl")
    def test_method_exclusion(self, mock_sl):
        """Test that method exclusions work."""
        mock_sl.get_available_schemas.return_value = ["team.json"]
        mock_sl.load_endpoint_model.return_value = {
            "team": {"teams": {"path": "/v1/teams"}},
        }
        mock_sl.load_stats_schema.return_value = {
            "apis": [
                {
                    "path": "/v1/teams",
                    "description": "teams",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "teams",
                            "summary": "Get teams",
                            "notes": "",
                            "parameters": [],
                        }
                    ],
                },
                {
                    "path": "/v1/teams/affiliates",
                    "description": "affiliates",
                    "operations": [
                        {
                            "method": "GET",
                            "nickname": "affiliates",
                            "summary": "Get affiliates",
                            "notes": "",
                            "parameters": [],
                        }
                    ],
                },
            ]
        }

        excluded = {"team": {"affiliates"}}

        team_endpoint = StatsAPI(excluded_methods=excluded).get_endpoint("team")
        assert "teams" in team_endpoint.get_method_names()
        assert "affiliates" not in team_endpoint.get_method_names()
