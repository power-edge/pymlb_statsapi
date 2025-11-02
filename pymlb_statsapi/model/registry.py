"""
Registry for MLB StatsAPI Endpoints.

This module automatically generates endpoint classes from JSON schemas.

Usage:
    from pymlb_statsapi import api

    # Use any endpoint
    response = api.Schedule.schedule(query_params={"sportId": 1, "date": "2025-06-01"})
    data = response.json()

    # Generate resource paths
    path = response.get_path(prefix="mlb-data")

    # Generate URIs for different protocols
    file_path = response.get_uri(protocol="file", prefix="mlb-data")
    s3_uri = response.get_uri(protocol="s3", prefix="raw-data", gzip=True)
    redis_key = response.get_uri(protocol="redis", prefix="mlb")
"""

from pymlb_statsapi.utils.log import LogMixin
from pymlb_statsapi.utils.schema_loader import sl

from .factory import Endpoint

# Configuration for methods to exclude (broken or unimplemented in API)
EXCLUDED_METHODS = {
    "team": {
        "affiliates",  # Broken in beta API - path doesn't match actual API
        "allTeams",  # Broken in beta API - path doesn't match actual API
    },
    "schedule": {
        # scheduleType has issues - documented in original code
    },
    # Add other exclusions as needed
}


class StatsAPI(LogMixin):
    """
    StatsAPI registry that generates endpoint classes from JSON schemas.

    Attributes:
        All endpoint names are available as attributes (e.g., .Schedule, .Game, .Team)
    """

    def __init__(self, excluded_methods: dict[str, set[str]] | None = None):
        """
        Initialize the dynamic API registry.

        Args:
            excluded_methods: Dict mapping endpoint names to sets of method names to exclude.
                             Defaults to EXCLUDED_METHODS if not provided.
        """
        super().__init__()
        self.excluded_methods = (
            excluded_methods if excluded_methods is not None else EXCLUDED_METHODS
        )
        self._endpoints: dict[str, Endpoint] = {}
        self._endpoint_config = sl.load_endpoint_model()
        self._initialize_endpoints()

    def _initialize_endpoints(self):
        """Load all available schemas and create endpoint instances."""
        # Get list of available schemas
        available_schemas = sl.get_available_schemas()

        for schema_file in available_schemas:
            # Extract endpoint name (remove .json extension)
            endpoint_name = schema_file.replace(".json", "")

            try:
                # Load the schema
                schema = sl.load_stats_schema(endpoint_name)

                # Get endpoint config
                endpoint_config = self._endpoint_config.get(endpoint_name, {})

                # Get excluded methods for this endpoint
                excluded = self.excluded_methods.get(endpoint_name, set())

                # Create dynamic endpoint
                endpoint = Endpoint(
                    endpoint_name=endpoint_name,
                    schema=schema,
                    endpoint_config=endpoint_config,
                    excluded_methods=excluded,
                )

                self._endpoints[endpoint_name] = endpoint

                # Add as attribute with capitalized name (e.g., schedule -> Schedule)
                attr_name = endpoint_name.capitalize()
                setattr(self, attr_name, endpoint)

                self.log.debug(f"Loaded endpoint: {attr_name} ({endpoint_name})")

            except Exception as e:
                self.log.error(f"Failed to load endpoint '{endpoint_name}': {e}")
                continue

    def get_endpoint_names(self) -> list[str]:
        """Get list of all loaded endpoint names."""
        return list(self._endpoints.keys())

    def get_endpoint(self, endpoint_name: str) -> Endpoint:
        """
        Get an endpoint by name.

        Args:
            endpoint_name: The endpoint name (lowercase, e.g., 'schedule')

        Returns:
            DynamicEndpoint instance

        Raises:
            KeyError: If endpoint not found
        """
        if endpoint_name not in self._endpoints:
            raise KeyError(
                f"Endpoint '{endpoint_name}' not found. Available: {self.get_endpoint_names()}"
            )
        return self._endpoints[endpoint_name]

    def list_all_methods(self) -> dict[str, list[str]]:
        """
        Get a mapping of all endpoints and their available methods.

        Returns:
            Dict mapping endpoint names to lists of method names
        """
        return {
            endpoint_name: endpoint.get_method_names()
            for endpoint_name, endpoint in self._endpoints.items()
        }

    def get_method_info(self, endpoint_name: str, method_name: str) -> dict:
        """
        Get detailed information about a specific method.

        Args:
            endpoint_name: The endpoint name (e.g., 'schedule')
            method_name: The method name (e.g., 'schedule')

        Returns:
            Dict with method details (path, parameters, etc.)
        """
        endpoint = self.get_endpoint(endpoint_name)
        return endpoint.get_method_info(method_name)

    def __repr__(self):
        endpoints = ", ".join(self.get_endpoint_names())
        return f"{self.__class__.__name__}(endpoints=[{endpoints}])"


# Create a singleton instance for convenient access
# This mimics the old StatsAPI usage pattern
api = StatsAPI()


# Alternative: Create a function that returns a new instance
def create_stats_api(excluded_methods: dict[str, set[str]] | None = None) -> StatsAPI:
    """
    Create a new StatsAPI instance.

    Args:
        excluded_methods: Optional custom exclusion mapping

    Returns:
        StatsAPI instance
    """
    return StatsAPI(excluded_methods=excluded_methods)
