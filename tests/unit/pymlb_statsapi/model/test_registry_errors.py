"""
Unit tests for StatsAPI registry error handling.
"""

from unittest.mock import patch

import pytest

from pymlb_statsapi import StatsAPI


class TestStatsAPIRegistry:
    """Test StatsAPI registry error handling."""

    @patch("pymlb_statsapi.model.registry.sl")
    def test_get_endpoint_not_found(self, mock_sl):
        """Test get_endpoint raises KeyError for non-existent endpoint."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}}
        }
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()

        with pytest.raises(KeyError, match="Endpoint 'nonexistent' not found"):
            registry.get_endpoint("nonexistent")

    @patch("pymlb_statsapi.model.registry.sl")
    def test_endpoint_loading_continues_on_error(self, mock_sl):
        """Test that registry continues loading endpoints even if one fails."""
        mock_sl.get_available_schemas.return_value = ["good.json", "bad.json", "another.json"]

        def mock_load_schema(name):
            if name == "bad":
                raise ValueError("Bad schema")
            return {"apis": []}

        mock_sl.load_stats_schema.side_effect = mock_load_schema
        mock_sl.load_endpoint_model.return_value = {
            "good": {},
            "bad": {},
            "another": {},
        }

        registry = StatsAPI()

        # Good and another should load, bad should be skipped
        endpoint_names = registry.get_endpoint_names()
        assert "good" in endpoint_names
        assert "another" in endpoint_names
        # bad may or may not be in the list depending on when the error occurred

    @patch("pymlb_statsapi.model.registry.sl")
    def test_get_endpoint_names(self, mock_sl):
        """Test get_endpoint_names returns all loaded endpoints."""
        mock_sl.get_available_schemas.return_value = ["schedule.json", "game.json", "person.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {},
            "game": {},
            "person": {},
        }
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()
        names = registry.get_endpoint_names()

        assert isinstance(names, list)
        assert "schedule" in names
        assert "game" in names
        assert "person" in names

    @patch("pymlb_statsapi.model.registry.sl")
    def test_endpoint_attribute_access(self, mock_sl):
        """Test accessing endpoints via attributes."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}}
        }
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()

        # Should be accessible via capitalized attribute
        assert hasattr(registry, "Schedule")
        endpoint = registry.Schedule
        assert endpoint is not None

    @patch("pymlb_statsapi.model.registry.sl")
    def test_endpoint_caching(self, mock_sl):
        """Test that endpoints are cached after first access."""
        mock_sl.get_available_schemas.return_value = ["schedule.json"]
        mock_sl.load_endpoint_model.return_value = {
            "schedule": {"schedule": {"path": "/v1/schedule"}}
        }
        mock_sl.load_stats_schema.return_value = {"apis": []}

        registry = StatsAPI()

        # Access endpoint twice
        endpoint1 = registry.get_endpoint("schedule")
        endpoint2 = registry.get_endpoint("schedule")

        # Should be the same object (cached)
        assert endpoint1 is endpoint2
