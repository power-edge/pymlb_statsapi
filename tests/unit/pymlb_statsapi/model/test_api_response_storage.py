"""
Unit tests for APIResponse storage methods (get_path, get_uri, save_json, gzip).
"""

import gzip as gzip_module
import json
import os
from unittest.mock import Mock
from urllib.parse import ParseResult

import pytest
import requests

from pymlb_statsapi.model.factory import APIResponse


class TestAPIResponseStorage:
    """Test APIResponse storage and path generation methods."""

    @pytest.fixture
    def mock_response(self):
        """Create a mock response for testing."""
        mock_resp = Mock(spec=requests.Response)
        mock_resp.url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-07-04"
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"dates": []}'
        mock_resp.elapsed = Mock()
        mock_resp.elapsed.total_seconds.return_value = 0.245
        mock_resp.json.return_value = {"dates": [{"date": "2024-07-04"}]}
        return mock_resp

    @pytest.fixture
    def api_response(self, mock_response):
        """Create an APIResponse for testing."""
        return APIResponse(
            response=mock_response,
            endpoint_name="schedule",
            method_name="schedule",
            path_params={},
            query_params={"sportId": "1", "date": "2024-07-04"},
        )

    def test_get_path_no_prefix(self, api_response):
        """Test get_path without prefix."""
        path = api_response.get_path()
        assert path == "schedule/schedule/date=2024-07-04&sportId=1"

    def test_get_path_with_prefix(self, api_response):
        """Test get_path with prefix."""
        path = api_response.get_path(prefix="mlb-data")
        assert path == "mlb-data/schedule/schedule/date=2024-07-04&sportId=1"

    def test_get_path_with_path_params(self, mock_response):
        """Test get_path with path parameters."""
        response = APIResponse(
            response=mock_response,
            endpoint_name="game",
            method_name="boxscore",
            path_params={"game_pk": "747175"},
            query_params={"fields": "gameData"},
        )
        path = response.get_path(prefix="data")
        assert path == "data/game/boxscore/game_pk=747175/fields=gameData"

    def test_get_path_no_params(self, mock_response):
        """Test get_path with no parameters."""
        response = APIResponse(
            response=mock_response,
            endpoint_name="sports",
            method_name="sports",
            path_params={},
            query_params={},
        )
        path = response.get_path()
        assert path == "sports/sports"

    def test_get_uri_default(self, api_response):
        """Test get_uri with defaults."""
        uri = api_response.get_uri()

        assert isinstance(uri, ParseResult)
        assert uri.scheme == "file"
        assert uri.netloc == ""
        assert uri.path.endswith("schedule/schedule/date=2024-07-04&sportId=1.json")
        assert ".var/local/mlb_statsapi" in uri.path

    def test_get_uri_with_prefix(self, api_response):
        """Test get_uri with prefix."""
        uri = api_response.get_uri(prefix="test-data")

        assert uri.scheme == "file"
        assert "test-data/schedule/schedule" in uri.path
        assert uri.path.endswith(".json")

    def test_get_uri_with_gzip(self, api_response):
        """Test get_uri with gzip extension."""
        uri = api_response.get_uri(gzip=True)

        assert uri.path.endswith(".json.gz")

    def test_get_uri_custom_base_path(self, api_response, tmp_path):
        """Test get_uri with custom base path from environment."""
        os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"] = str(tmp_path)

        try:
            uri = api_response.get_uri()
            assert str(tmp_path) in uri.path
        finally:
            del os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"]

    def test_save_json_auto_path(self, api_response, tmp_path):
        """Test save_json with auto-generated path."""
        os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"] = str(tmp_path)

        try:
            result = api_response.save_json(prefix="test")

            assert "path" in result
            assert "bytes_written" in result
            assert "timestamp" in result
            assert "uri" in result
            assert isinstance(result["uri"], ParseResult)

            # Verify file was created
            assert os.path.exists(result["path"])

            # Verify content structure
            with open(result["path"]) as f:
                data = json.load(f)
                assert "metadata" in data
                assert "data" in data
                assert data["data"]["dates"] == [{"date": "2024-07-04"}]
        finally:
            del os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"]

    def test_save_json_explicit_path(self, api_response, tmp_path):
        """Test save_json with explicit file path."""
        file_path = tmp_path / "test.json"

        result = api_response.save_json(file_path=str(file_path))

        assert result["path"] == str(file_path)
        assert "uri" not in result  # URI only included when auto-generating
        assert os.path.exists(file_path)

    def test_save_json_gzipped(self, api_response, tmp_path):
        """Test save_json with gzip compression."""
        os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"] = str(tmp_path)

        try:
            result = api_response.save_json(gzip=True, prefix="compressed")

            assert result["path"].endswith(".json.gz")
            assert os.path.exists(result["path"])

            # Verify gzipped content
            with gzip_module.open(result["path"], "rt", encoding="utf-8") as f:
                data = json.load(f)
                assert "metadata" in data
                assert "data" in data
        finally:
            del os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"]

    def test_save_json_creates_parent_dirs(self, api_response, tmp_path):
        """Test save_json creates parent directories."""
        file_path = tmp_path / "nested" / "dirs" / "test.json"

        api_response.save_json(file_path=str(file_path))

        assert os.path.exists(file_path)
        assert file_path.parent.exists()

    def test_gzip_convenience_method(self, api_response, tmp_path):
        """Test gzip() convenience method."""
        os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"] = str(tmp_path)

        try:
            result = api_response.gzip(prefix="data")

            assert result["path"].endswith(".json.gz")
            assert os.path.exists(result["path"])

            # Verify it's properly gzipped
            with gzip_module.open(result["path"], "rt", encoding="utf-8") as f:
                data = json.load(f)
                assert "metadata" in data
                assert "data" in data
        finally:
            del os.environ["PYMLB_STATSAPI__BASE_FILE_PATH"]

    def test_gzip_with_explicit_path(self, api_response, tmp_path):
        """Test gzip() with explicit file path."""
        file_path = tmp_path / "explicit.json.gz"

        result = api_response.gzip(file_path=str(file_path))

        assert result["path"] == str(file_path)
        assert os.path.exists(file_path)

    def test_metadata_in_saved_file(self, api_response, tmp_path):
        """Test that saved files include complete metadata."""
        file_path = tmp_path / "metadata_test.json"

        api_response.save_json(file_path=str(file_path))

        with open(file_path) as f:
            data = json.load(f)

        # Check metadata structure
        assert "metadata" in data
        assert "request" in data["metadata"]
        assert "response" in data["metadata"]

        # Check request metadata
        req = data["metadata"]["request"]
        assert req["endpoint_name"] == "schedule"
        assert req["method_name"] == "schedule"
        assert req["query_params"] == {"sportId": "1", "date": "2024-07-04"}
        assert "timestamp" in req

        # Check response metadata
        resp = data["metadata"]["response"]
        assert resp["status_code"] == 200
        assert resp["ok"] is True
        assert "elapsed_ms" in resp
