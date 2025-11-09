"""
Unit tests for EndpointMethod introspection methods (get_parameter_schema, list_parameters, get_long_description).
"""

import pytest

from pymlb_statsapi.model.factory import EndpointMethod


class TestEndpointMethodIntrospection:
    """Test EndpointMethod introspection and documentation methods."""

    @pytest.fixture
    def sample_method(self):
        """Create a sample EndpointMethod for testing."""
        api_def = {"path": "/v1/game/{game_pk}/boxscore"}
        operation_def = {
            "method": "GET",
            "summary": "Get boxscore for a game",
            "notes": "Returns detailed boxscore information including teams, players, and stats.",
            "parameters": [
                {
                    "name": "game_pk",
                    "paramType": "path",
                    "type": "integer",
                    "required": True,
                    "description": "Unique game identifier",
                },
                {
                    "name": "fields",
                    "paramType": "query",
                    "type": "string",
                    "required": False,
                    "description": "Comma-separated list of fields to include",
                },
                {
                    "name": "timecode",
                    "paramType": "query",
                    "type": "string",
                    "required": False,
                    "enum": ["now", "YYYYMMDD_HHMMSS"],
                    "description": "Time code for historical data",
                },
            ],
        }

        return EndpointMethod(
            endpoint_name="game",
            method_name="boxscore",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/game/{game_pk}/boxscore",
        )

    def test_get_parameter_schema_path_param(self, sample_method):
        """Test get_parameter_schema for path parameter."""
        param = sample_method.get_parameter_schema("game_pk")

        assert param is not None
        assert param["name"] == "game_pk"
        assert param["paramType"] == "path"
        assert param["type"] == "integer"
        assert param["required"] is True
        assert param["description"] == "Unique game identifier"

    def test_get_parameter_schema_query_param(self, sample_method):
        """Test get_parameter_schema for query parameter."""
        param = sample_method.get_parameter_schema("fields")

        assert param is not None
        assert param["name"] == "fields"
        assert param["paramType"] == "query"
        assert param["type"] == "string"
        assert param["required"] is False

    def test_get_parameter_schema_not_found(self, sample_method):
        """Test get_parameter_schema returns None for non-existent parameter."""
        param = sample_method.get_parameter_schema("nonexistent")

        assert param is None

    def test_get_parameter_schema_returns_copy(self, sample_method):
        """Test that get_parameter_schema returns a copy, not reference."""
        param1 = sample_method.get_parameter_schema("game_pk")
        param2 = sample_method.get_parameter_schema("game_pk")

        # Modify one copy
        param1["modified"] = True

        # Other copy should be unchanged
        assert "modified" not in param2

    def test_list_parameters(self, sample_method):
        """Test list_parameters returns organized parameter list."""
        params = sample_method.list_parameters()

        # Check structure
        assert "path" in params
        assert "query" in params
        assert isinstance(params["path"], list)
        assert isinstance(params["query"], list)

        # Check path parameters
        assert len(params["path"]) == 1
        path_param = params["path"][0]
        assert path_param["name"] == "game_pk"
        assert path_param["type"] == "integer"
        assert path_param["required"] is True
        assert path_param["description"] == "Unique game identifier"

        # Check query parameters
        assert len(params["query"]) == 2
        query_names = [p["name"] for p in params["query"]]
        assert "fields" in query_names
        assert "timecode" in query_names

    def test_list_parameters_default_values(self):
        """Test list_parameters provides defaults for missing fields."""
        api_def = {"path": "/v1/sports"}
        operation_def = {
            "method": "GET",
            "summary": "Get sports",
            "notes": "",
            "parameters": [
                {
                    "name": "sportId",
                    "paramType": "query",
                    # Missing type, required, description
                }
            ],
        }

        method = EndpointMethod(
            endpoint_name="sports",
            method_name="sports",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/sports",
        )

        params = method.list_parameters()
        query_param = params["query"][0]

        assert query_param["name"] == "sportId"
        assert query_param["type"] == "string"  # Default
        assert query_param["required"] is False  # Default
        assert query_param["description"] == ""  # Default

    def test_list_parameters_empty(self):
        """Test list_parameters with no parameters."""
        api_def = {"path": "/v1/sports"}
        operation_def = {
            "method": "GET",
            "summary": "Get sports",
            "notes": "",
            "parameters": [],
        }

        method = EndpointMethod(
            endpoint_name="sports",
            method_name="sports",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/sports",
        )

        params = method.list_parameters()

        assert params["path"] == []
        assert params["query"] == []

    def test_get_long_description(self, sample_method):
        """Test get_long_description generates comprehensive documentation."""
        description = sample_method.get_long_description()

        # Check that key information is included
        assert "boxscore" in description
        assert "Get boxscore for a game" in description
        assert "Returns detailed boxscore information" in description
        assert "/v1/game/{game_pk}/boxscore" in description

        # Check parameters are documented
        assert "game_pk" in description
        assert "fields" in description
        assert "timecode" in description

        # Check parameter details
        assert "path" in description.lower()
        assert "query" in description.lower()
        assert "integer" in description
        assert "string" in description

    def test_get_long_description_minimal(self):
        """Test get_long_description with minimal schema."""
        api_def = {"path": "/v1/sports"}
        operation_def = {
            "method": "GET",
            "summary": "Get sports",
            "notes": "",
            "parameters": [],
        }

        method = EndpointMethod(
            endpoint_name="sports",
            method_name="sports",
            api_definition=api_def,
            operation_definition=operation_def,
            config_path="/v1/sports",
        )

        description = method.get_long_description()

        assert "sports" in description
        assert "Get sports" in description
        assert "/v1/sports" in description

    def test_get_schema(self, sample_method):
        """Test get_schema returns complete schema structure."""
        schema = sample_method.get_schema()

        # Check structure
        assert "endpoint" in schema
        assert "method" in schema
        assert "api" in schema
        assert "operation" in schema
        assert "config_path" in schema

        # Check values
        assert schema["endpoint"] == "game"
        assert schema["method"] == "boxscore"
        assert schema["operation"]["method"] == "GET"
        assert schema["operation"]["summary"] == "Get boxscore for a game"
        assert len(schema["operation"]["parameters"]) == 3

    def test_method_properties(self, sample_method):
        """Test that method properties are accessible."""
        assert sample_method.endpoint_name == "game"
        assert sample_method.method_name == "boxscore"
        assert sample_method.http_method == "GET"
        assert len(sample_method.path_params) == 1
        assert len(sample_method.query_params) == 2
