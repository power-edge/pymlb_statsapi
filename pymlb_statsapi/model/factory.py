"""
Dynamic model generation for MLB StatsAPI endpoints.

This module provides a fully config-driven approach to generating endpoint classes
and methods from JSON schemas, eliminating hardcoded model definitions.

Key features:
- Dynamic class and method generation from JSON schemas
- Response objects with URL metadata for caching
- Configurable method exclusions
- Automatic parameter validation from schemas
"""

import gzip as gzip_module
import json
import os
from datetime import UTC, datetime
from time import sleep
from urllib.parse import ParseResult, urlencode, urlparse

import requests

from pymlb_statsapi.utils.log import LogMixin


class APIResponse(LogMixin):
    """
    MLB Stats API Response wrapper that includes URL metadata for caching and debugging.

    This approach that just wraps the `requests.Response`
    and provides convenient access to URL components for cache key generation.
    """

    def __init__(
        self,
        response: requests.Response,
        endpoint_name: str,
        method_name: str,
        path_params: dict | None = None,
        query_params: dict | None = None,
    ):
        super().__init__()
        self.response = response
        self.endpoint_name = endpoint_name
        self.method_name = method_name
        self.path_params = path_params or {}
        self.query_params = query_params or {}
        self.timestamp = datetime.now(UTC).isoformat()

        # Parse URL components
        parsed = urlparse(response.url)
        self.scheme = parsed.scheme
        self.domain = parsed.netloc
        self.path = parsed.path
        self.url = response.url

    def __repr__(self):
        return f"{self.__class__.__name__}(endpoint={self.endpoint_name}, method={self.method_name}, status={self.status_code}, url={self.url})"

    @property
    def status_code(self) -> int:
        """HTTP status code"""
        return self.response.status_code

    @property
    def ok(self) -> bool:
        """True if status code is 2xx"""
        return self.response.ok

    def json(self) -> dict | list:
        """Parse response as JSON"""
        data = self.response.json()
        # Remove copyright notice if present
        if isinstance(data, dict) and "copyright" in data:
            data.pop("copyright")
        return data

    @property
    def text(self) -> str:
        """Response body as text"""
        return self.response.text

    @property
    def content(self) -> bytes:
        """Response body as bytes"""
        return self.response.content

    @property
    def headers(self) -> dict:
        """Response headers"""
        return dict(self.response.headers)

    def get_metadata(self) -> dict:
        """
        Get all request and response metadata as a JSON-serializable dict.

        This includes everything about the request and response except the actual data payload.
        Consumers can use this metadata to build cache keys, store provenance, track API usage, etc.

        Returns:
            dict: Metadata with the following structure:
                - request: Request metadata (endpoint, method, params, url, timestamp)
                - response: Response metadata (status_code, headers, elapsed, content_length)

        Example:
            >>> response = StatsAPI.Schedule.schedule(sportId=1, date="2025-06-01")
            >>> metadata = response.get_metadata()
            >>> print(json.dumps(metadata, indent=2))
            {
              "request": {
                "endpoint_name": "schedule",
                "method_name": "schedule",
                "path_params": {},
                "query_params": {"sportId": "1", "date": "2025-06-01"},
                "url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-06-01",
                "scheme": "https",
                "domain": "statsapi.mlb.com",
                "path": "/api/v1/schedule",
                "http_method": "GET",
                "timestamp": "2025-01-15T10:30:00.123456+00:00"
              },
              "response": {
                "status_code": 200,
                "ok": true,
                "elapsed_ms": 245.3,
                "content_type": "application/json",
                "content_length": 15234,
                "headers": {...}
              }
            }
        """
        return {
            "request": {
                "endpoint_name": self.endpoint_name,
                "method_name": self.method_name,
                "path_params": dict(self.path_params),
                "query_params": dict(self.query_params),
                "url": self.url,
                "scheme": self.scheme,
                "domain": self.domain,
                "path": self.path,
                "http_method": "GET",  # Currently always GET
                "timestamp": self.timestamp,
            },
            "response": {
                "status_code": self.status_code,
                "ok": self.ok,
                "elapsed_ms": self.response.elapsed.total_seconds() * 1000,
                "content_type": self.response.headers.get("Content-Type"),
                "content_length": len(self.response.content),
                "headers": self.headers,
            },
        }

    def to_dict(self, include_data: bool = True) -> dict:
        """
        Convert the entire APIResponse to a JSON-serializable dict.

        This is the primary method consumers should use to serialize the complete
        response (metadata + data) for storage, caching, or transmission.

        Args:
            include_data: Whether to include the response data payload (default: True)
                         Set to False to get only metadata (equivalent to get_metadata())

        Returns:
            dict: Complete response with metadata and data:
                - metadata: All request/response metadata (from get_metadata())
                - data: The parsed JSON response data (if include_data=True)

        Example:
            >>> response = StatsAPI.Schedule.schedule(sportId=1, date="2025-06-01")
            >>> # Get everything
            >>> full_dict = response.to_dict()
            >>> # Save to your storage
            >>> with open("my_cache.json", "w") as f:
            >>>     json.dump(full_dict, f)
            >>>
            >>> # Or just metadata
            >>> metadata_only = response.to_dict(include_data=False)
        """
        result = {
            "metadata": self.get_metadata(),
        }
        if include_data:
            result["data"] = self.json()
        return result

    def get_path(self, prefix: str = "") -> str:
        """
        Generate a resource path for this API response.

        The path does NOT include file extensions - those are added by get_uri() for
        file/s3 protocols. This keeps the path protocol-agnostic and flexible.

        Format: {prefix}/{endpoint}/{method}/{path_params}/{sorted_query_params}

        Examples:
            - schedule/schedule/sportId=1&date=2025-06-01
            - mlb-data/schedule/schedule/sportId=1&date=2025-06-01
            - game/liveGameV1/game_pk=12345/timecode=20250601_120000

        Args:
            prefix: Optional prefix to prepend (separated by /)

        Returns:
            Path string suitable for use across different storage protocols
        """
        parts = []
        if prefix:
            parts.append(prefix)

        parts.extend([self.endpoint_name, self.method_name])

        # Add path params (sorted for consistency)
        if self.path_params:
            path_str = "&".join(f"{k}={v}" for k, v in sorted(self.path_params.items()))
            parts.append(path_str)

        # Add query params (sorted for consistency)
        if self.query_params:
            query_str = "&".join(f"{k}={v}" for k, v in sorted(self.query_params.items()))
            parts.append(query_str)

        return "/".join(parts)

    def get_uri(self, prefix: str = "", gzip: bool = False) -> ParseResult:
        """
        Generate full file URI as a ParseResult for this API response.

        Returns a urllib.parse.ParseResult that provides structured access to all URI components:
        - scheme: 'file'
        - netloc: '' (empty for file protocol)
        - path: the absolute file path

        Args:
            prefix: Optional directory prefix
            gzip: Whether to add .gz extension (default: False)

        Environment Variables:
            PYMLB_STATSAPI__BASE_FILE_PATH: Base directory for storage
                                           (default: ./.var/local/mlb_statsapi)

        Returns:
            ParseResult object with URI components. Call .geturl() to get string representation.

        Examples:
            >>> result = response.get_uri(prefix="mlb-data")
            >>> result.scheme
            'file'
            >>> result.path
            '/path/to/.var/local/mlb_statsapi/mlb-data/schedule/schedule/date=2025-06-01.json'
            >>> result.geturl()
            'file:///path/to/.var/local/mlb_statsapi/mlb-data/schedule/schedule/date=2025-06-01.json'

            >>> result = response.get_uri(gzip=True)
            >>> result.path
            '/path/to/.var/local/mlb_statsapi/schedule/schedule/date=2025-06-01.json.gz'
        """
        resource_path = self.get_path(prefix=prefix)

        base_path = os.environ.get("PYMLB_STATSAPI__BASE_FILE_PATH", "./.var/local/mlb_statsapi")
        extension = ".json.gz" if gzip else ".json"
        full_path = os.path.join(base_path, resource_path + extension)

        # For file URLs, path should start with /
        if not full_path.startswith("/"):
            full_path = os.path.abspath(full_path)

        return ParseResult(
            scheme="file", netloc="", path=full_path, params="", query="", fragment=""
        )

    def save_json(self, file_path: str | None = None, gzip: bool = False, prefix: str = "") -> dict:
        """
        Save response JSON to a file.

        Args:
            file_path: Path to save the JSON file. If None, auto-generates using get_uri().
            gzip: Whether to gzip the output (default: False)
            prefix: Optional directory prefix (only used if file_path is None)

        Returns:
            Dict with 'path', 'bytes_written', and 'uri' (ParseResult) keys

        Examples:
            >>> # Save to explicit path
            >>> response.save_json("/path/to/file.json")

            >>> # Auto-generate path
            >>> response.save_json(prefix="mlb-data")

            >>> # Save gzipped with custom prefix
            >>> response.save_json(gzip=True, prefix="raw-data")

            >>> # Get URI details when auto-generating
            >>> result = response.save_json(prefix="mlb-data")
            >>> result['path']  # String path
            >>> result['uri'].scheme  # 'file'
            >>> result['uri'].geturl()  # Full file:// URI
        """
        uri = None
        if file_path is None:
            # Auto-generate path using get_uri()
            uri = self.get_uri(prefix=prefix, gzip=gzip)
            # Extract path from ParseResult
            file_path = uri.path

        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Prepare data with metadata wrapper
        data_with_metadata = {
            "metadata": self.get_metadata(),
            "data": self.json(),
        }

        if gzip:
            with gzip_module.open(file_path, "wt", encoding="utf-8") as f:
                content = json.dumps(data_with_metadata, indent=2)
                bytes_written = f.write(content)
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                content = json.dumps(data_with_metadata, indent=2)
                bytes_written = f.write(content)

        self.log.info(f"Saved {self} to {file_path} (gzip={gzip})")
        result = {
            "path": file_path,
            "bytes_written": bytes_written,
            "timestamp": self.timestamp,
        }
        if uri:
            result["uri"] = uri
        return result

    def gzip(self, file_path: str | None = None, prefix: str = "") -> dict:
        """
        Save response as gzipped JSON (convenience method).

        This is equivalent to calling save_json(gzip=True, ...).

        Args:
            file_path: Path to save the gzipped JSON file. If None, auto-generates.
            prefix: Optional directory prefix (only used if file_path is None)

        Returns:
            Dict with 'path', 'bytes_written', and 'uri' keys

        Examples:
            >>> response.gzip("/path/to/file.json.gz")
            >>> response.gzip(prefix="mlb-data")  # Auto-generates path
        """
        return self.save_json(file_path=file_path, gzip=True, prefix=prefix)


class EndpointMethod:
    """
    Represents a single API method with its schema-defined parameters and validation.
    """

    def __init__(
        self,
        endpoint_name: str,
        method_name: str,
        api_definition: dict,
        operation_definition: dict,
        config_path: str,
    ):
        self.endpoint_name = endpoint_name
        self.method_name = method_name

        # Store original schema JSON for documentation and introspection
        # Users can access this to see the full API definition
        self._schema_api = api_definition.copy()  # Original API definition
        self._schema_operation = operation_definition.copy()  # Original operation definition

        # Keep references for backward compatibility
        self.api_definition = api_definition
        self.operation = operation_definition
        self.config_path = config_path

        # Extract path and operation details
        # Use config_path if provided, otherwise fall back to api_definition path
        self.path_template = config_path if config_path else api_definition["path"]
        self.http_method = operation_definition["method"]
        self.summary = operation_definition.get("summary", "")
        self.notes = operation_definition.get("notes", "")

        # Parse parameters - IMPORTANT: Preserve exact parameter names from schema
        # Do NOT convert camelCase to snake_case (e.g., keep "sportId", not "sport_id")
        self.path_params = [
            p for p in operation_definition.get("parameters", []) if p["paramType"] == "path"
        ]
        self.query_params = [
            p for p in operation_definition.get("parameters", []) if p["paramType"] == "query"
        ]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.endpoint_name}.{self.method_name}, path={self.path_template})"

    def get_schema(self) -> dict:
        """
        Get the original schema JSON that defines this method.

        Returns a dict with:
        - api: The API definition (path, description)
        - operation: The operation definition (method, parameters, etc.)
        - endpoint: Endpoint name
        - method: Method name
        - config_path: Configured path (if different from schema)

        Returns:
            dict: Complete schema definition

        Example:
            >>> method = api.Schedule.get_method_info("schedule")
            >>> schema = method.get_schema()
            >>> print(schema["operation"]["summary"])
            'View schedule info'
            >>> for param in schema["operation"]["parameters"]:
            ...     print(f"{param['name']}: {param['description']}")
        """
        return {
            "endpoint": self.endpoint_name,
            "method": self.method_name,
            "api": self._schema_api,
            "operation": self._schema_operation,
            "config_path": self.config_path,
        }

    def get_parameter_schema(self, param_name: str) -> dict | None:
        """
        Get the full schema definition for a specific parameter.

        Args:
            param_name: Name of the parameter (e.g., "sportId", "date")

        Returns:
            dict with parameter details or None if not found

        Example:
            >>> param = method.get_parameter_schema("sportId")
            >>> print(param["description"])
            'Top level organization of a sport'
            >>> print(param["required"])
            False
            >>> print(param["type"])
            'integer'
        """
        all_params = self._schema_operation.get("parameters", [])
        for param in all_params:
            if param["name"] == param_name:
                return param.copy()
        return None

    def list_parameters(self) -> dict:
        """
        List all parameters with their types and whether they're required.

        Returns:
            dict with 'path' and 'query' keys, each containing parameter info

        Example:
            >>> params = method.list_parameters()
            >>> for param in params["path"]:
            ...     print(f"{param['name']} ({param['type']}): {param['required']}")
            >>> for param in params["query"]:
            ...     print(f"{param['name']} ({param['type']}): {param['required']}")
        """
        return {
            "path": [
                {
                    "name": p["name"],
                    "type": p.get("type", "string"),
                    "required": p.get("required", False),
                    "description": p.get("description", ""),
                }
                for p in self.path_params
            ],
            "query": [
                {
                    "name": p["name"],
                    "type": p.get("type", "string"),
                    "required": p.get("required", False),
                    "description": p.get("description", ""),
                }
                for p in self.query_params
            ],
        }

    def get_long_description(self) -> str:
        """
        Get a comprehensive description of this method including all schema details.

        Returns a formatted string with:
        - Summary
        - Notes
        - HTTP method and path
        - All parameters with descriptions
        - Response information

        Returns:
            str: Formatted description

        Example:
            >>> print(method.get_long_description())
        """
        lines = []
        lines.append(f"{'=' * 70}")
        lines.append(f"{self.endpoint_name}.{self.method_name}")
        lines.append(f"{'=' * 70}")
        lines.append("")

        lines.append(f"Summary: {self.summary}")
        if self.notes:
            lines.append(f"Notes: {self.notes}")
        lines.append("")

        lines.append(f"HTTP Method: {self.http_method}")
        lines.append(f"Path: {self.path_template}")
        lines.append("")

        if self.path_params:
            lines.append("Path Parameters:")
            for param in self.path_params:
                required = "REQUIRED" if param.get("required") else "optional"
                param_type = param.get("type", "string")
                desc = param.get("description", "No description")
                lines.append(f"  - {param['name']} ({param_type}, {required})")
                lines.append(f"    {desc}")
                if "enum" in param and param["enum"]:
                    lines.append(f"    Allowed values: {', '.join(str(v) for v in param['enum'])}")
            lines.append("")

        if self.query_params:
            lines.append("Query Parameters:")
            for param in self.query_params:
                required = "REQUIRED" if param.get("required") else "optional"
                param_type = param.get("type", "string")
                desc = param.get("description", "No description")
                lines.append(f"  - {param['name']} ({param_type}, {required})")
                lines.append(f"    {desc}")
                if "enum" in param and param["enum"]:
                    lines.append(f"    Allowed values: {', '.join(str(v) for v in param['enum'])}")
                if param.get("allowMultiple"):
                    lines.append("    Allows multiple values (comma-separated)")
            lines.append("")

        # Response info
        response_messages = self._schema_operation.get("responseMessages", [])
        if response_messages:
            lines.append("Response Codes:")
            for msg in response_messages:
                code = msg.get("code", "?")
                message = msg.get("message", "")
                lines.append(f"  - {code}: {message}")
            lines.append("")

        lines.append(f"{'=' * 70}")

        return "\n".join(lines)

    def validate_and_resolve_params(
        self,
        path_params: dict | None = None,
        query_params: dict | None = None,
    ) -> tuple[dict, dict, str]:
        """
        Validate parameters and resolve the full URL path.

        Args:
            path_params: Path parameter values
            query_params: Query parameter values

        Returns:
            Tuple of (validated_path_params, validated_query_params, resolved_path)

        Raises:
            AssertionError: If required parameters are missing or invalid
        """
        path_params = dict(path_params or {})
        query_params = dict(query_params or {})

        # Validate path parameters
        validated_path_params = {}
        for param_def in self.path_params:
            param_name = param_def["name"]

            if param_def["required"] and param_name not in path_params:
                raise AssertionError(
                    f"{self.method_name}: path parameter '{param_name}' is required"
                )

            if param_name in path_params:
                value = path_params.pop(param_name)

                # Handle list values (should only have one item for path params)
                if isinstance(value, list):
                    if len(value) != 1:
                        raise AssertionError(
                            f"{self.method_name}: path parameter '{param_name}' must have exactly one value, got {value}"
                        )
                    value = value[0]

                # Validate enum if present
                if "enum" in param_def and param_def["enum"]:
                    valid_values = {str(v).lower() for v in param_def["enum"]}
                    if str(value).lower() not in valid_values:
                        raise AssertionError(
                            f"{self.method_name}: '{param_name}' must be one of {param_def['enum']}, got '{value}'"
                        )

                validated_path_params[param_name] = str(value)

        # Check for unrecognized path params
        if path_params:
            raise AssertionError(
                f"{self.method_name}: unrecognized path parameters: {list(path_params.keys())}"
            )

        # Validate query parameters
        validated_query_params = {}
        for param_def in self.query_params:
            param_name = param_def["name"]

            if param_def["required"] and param_name not in query_params:
                raise AssertionError(
                    f"{self.method_name}: query parameter '{param_name}' is required"
                )

            if param_name in query_params:
                value = query_params.pop(param_name)

                # Handle list values
                if isinstance(value, list):
                    allow_multiple = param_def.get("allowMultiple", False)
                    if not allow_multiple and len(value) > 1:
                        raise AssertionError(
                            f"{self.method_name}: query parameter '{param_name}' does not allow multiple values"
                        )
                    value = ",".join(str(v) for v in value)
                else:
                    value = str(value)

                validated_query_params[param_name] = value

        # Check for unrecognized query params
        if query_params:
            raise AssertionError(
                f"{self.method_name}: unrecognized query parameters: {list(query_params.keys())}"
            )

        # Resolve path with parameters
        resolved_path = self.path_template.format(**validated_path_params)

        return validated_path_params, validated_query_params, resolved_path


class Endpoint(LogMixin):
    """
    Dynamically generated endpoint class that creates methods from JSON schema.
    """

    BASE_URL = "https://statsapi.mlb.com/api"
    MAX_RETRIES = int(os.environ.get("PYMLB_STATSAPI__MAX_RETRIES", "3"))
    TIMEOUT = int(os.environ.get("PYMLB_STATSAPI__TIMEOUT", "30"))

    def __init__(
        self,
        endpoint_name: str,
        schema: dict,
        endpoint_config: dict,
        excluded_methods: set[str] | None = None,
    ):
        super().__init__()
        self.endpoint_name = endpoint_name
        self.schema = schema
        self.endpoint_config = endpoint_config
        self.excluded_methods = excluded_methods or set()

        # Build method registry
        self._methods: dict[str, EndpointMethod] = {}
        self._initialize_methods()

    def _initialize_methods(self):
        """Build the method registry from schema and config."""
        # First pass: collect all operations and detect duplicates
        operations_by_nickname = {}
        for api in self.schema.get("apis", []):
            for operation in api.get("operations", []):
                # Only support GET methods for now
                if operation["method"] != "GET":
                    continue

                nickname = operation["nickname"]
                if nickname not in operations_by_nickname:
                    operations_by_nickname[nickname] = []
                operations_by_nickname[nickname].append((api, operation))

        # Detect which nicknames have duplicates for logging
        duplicate_nicknames = {
            nickname for nickname, ops in operations_by_nickname.items() if len(ops) > 1
        }

        if duplicate_nicknames:
            self.log.debug(
                f"{self.endpoint_name}: Found {len(duplicate_nicknames)} overloaded methods: "
                f"{', '.join(sorted(duplicate_nicknames))}"
            )

        # Second pass: create methods with disambiguation if needed
        import re

        for nickname, operations in operations_by_nickname.items():
            # Skip if explicitly excluded
            if nickname in self.excluded_methods:
                self.log.debug(f"Skipping excluded method: {self.endpoint_name}.{nickname}")
                continue

            # If only one operation, no disambiguation needed
            if len(operations) == 1:
                api, operation = operations[0]
                config_entry = self.endpoint_config.get(nickname, {})
                config_path = config_entry.get("path", api["path"])

                endpoint_method = EndpointMethod(
                    endpoint_name=self.endpoint_name,
                    method_name=nickname,
                    api_definition=api,
                    operation_definition=operation,
                    config_path=config_path,
                )
                self._methods[nickname] = endpoint_method
                self._add_method(nickname, endpoint_method)
                continue

            # Multiple operations with same nickname
            # For overloaded methods, use schema paths directly (not config paths)
            # since config can only map one path per nickname
            method_variants = []
            for api, operation in operations:
                # Use API path from schema for overloaded methods
                config_path = api["path"]
                path_params = re.findall(r"\{(\w+)\}", config_path)

                endpoint_method = EndpointMethod(
                    endpoint_name=self.endpoint_name,
                    method_name=nickname,
                    api_definition=api,
                    operation_definition=operation,
                    config_path=config_path,
                )
                method_variants.append((path_params, endpoint_method))

            # Sort by number of path params (base version first)
            method_variants.sort(key=lambda x: len(x[0]))

            # Create an overloaded method that routes based on provided path_params
            self._add_overloaded_method(nickname, method_variants)

            # Store all variants for introspection
            for path_params, method in method_variants:
                suffix = "_" + "_".join(path_params) if path_params else "_base"
                internal_name = f"__{nickname}{suffix}"
                self._methods[internal_name] = method

    def _add_overloaded_method(
        self, method_name: str, method_variants: list[tuple[list[str], EndpointMethod]]
    ):
        """
        Create an overloaded method with clean signature that routes based on arguments.

        Args:
            method_name: The method name
            method_variants: List of (path_param_names, endpoint_method) tuples, sorted by param count
        """
        # Collect all unique parameters across all variants
        all_path_params = set()
        all_query_params = set()

        for _, endpoint_method in method_variants:
            for p in endpoint_method.path_params:
                all_path_params.add(p["name"])
            for p in endpoint_method.query_params:
                all_query_params.add(p["name"])

        # Some params might appear in both path and query across different variants
        # Keep them all, but only add each unique name once to signature
        all_unique_params = all_path_params | all_query_params

        # Build signature with all possible params (all optional since variants differ)
        sig_parts = []

        # All params are optional keyword args (since different variants use different params)
        for param_name in sorted(all_unique_params):
            sig_parts.append(f"{param_name}=None")

        signature = ", ".join(sig_parts)

        # Build routing logic
        all_params_list = ", ".join(f"'{p}'" for p in sorted(all_unique_params))

        # Generate overloaded function
        func_code = f"""
def overloaded_impl({signature}):
    # Collect all provided params
    all_provided = {{}}
    for name in [{all_params_list}]:
        value = locals().get(name)
        if value is not None:
            all_provided[name] = value

    # Try to match a variant based on path params
    # For each variant, check if all its path params are provided
    for path_param_names, endpoint_method in variants:
        variant_path_set = set(path_param_names)
        provided_keys = set(all_provided.keys())

        # Check if all path params for this variant are provided
        # Also check that no extra path params from other variants are provided
        if variant_path_set.issubset(provided_keys):
            # Build path_params dict for this variant
            path_params = {{}}
            for name in path_param_names:
                path_params[name] = all_provided[name]

            # Build query_params dict - everything else that's not a path param for this variant
            query_params = {{}}
            variant_query_param_names = set(p["name"] for p in endpoint_method.query_params)
            for name, value in all_provided.items():
                if name not in path_param_names and name in variant_query_param_names:
                    query_params[name] = value

            return endpoint._execute_request(
                endpoint_method=endpoint_method,
                path_params=path_params if path_params else None,
                query_params=query_params if query_params else None,
            )

    # No match - provide helpful error
    param_options = [
        f"  - Path params: {{', '.join(params) or 'none'}}"
        for params, _ in variants
    ]
    raise AssertionError(
        f"{{endpoint_name}}.{{method_name}}: No matching variant for provided params={{set(all_provided.keys())}}.\\n"
        f"Available variants:\\n" + "\\n".join(param_options)
    )
"""

        # Execute with closure
        namespace = {
            "endpoint": self,
            "variants": method_variants,
            "endpoint_name": self.endpoint_name,
            "method_name": method_name,
        }
        exec(func_code, namespace)  # nosec B102 - Safe: func_code is generated internally from schema
        overloaded_func = namespace["overloaded_impl"]

        # Build docstring
        variant_docs = []
        for param_names, endpoint_method in method_variants:
            param_str = f"[{', '.join(param_names)}]" if param_names else "[base]"
            variant_docs.append(f"    Variant {param_str}: {endpoint_method.path_template}")

        overloaded_func.__name__ = method_name
        overloaded_func.__doc__ = f"""Overloaded method with {len(method_variants)} variants.

{chr(10).join(variant_docs)}

Call with appropriate parameters to route to the correct variant.
Provide the path parameters for your desired variant, plus any query parameters.

Args:
    Parameters (optional): {", ".join(sorted(all_unique_params)) if all_unique_params else "None"}
    Note: Which parameters are path vs query depends on the variant matched.

Returns:
    APIResponse: Response object with .json(), .save_json(), and .get_uri() methods
        """

        # Attach to instance
        setattr(self, method_name, overloaded_func)

        # Also store in _methods dict for the primary variant (usually base)
        self._methods[method_name] = method_variants[0][1]

    def _add_method(self, method_name: str, endpoint_method: EndpointMethod):
        """Dynamically add a method with clean signature - all params as direct arguments."""

        # Create function with schema-driven signature
        method_func = self._create_method_with_signature(endpoint_method)

        # Set method metadata
        method_func.__name__ = method_name
        method_func.__doc__ = self._build_method_docstring(endpoint_method)

        # Attach method to instance
        setattr(self, method_name, method_func)

    def _create_method_with_signature(self, endpoint_method: EndpointMethod):
        """
        Create a function where all parameters become direct function arguments.

        The schema defines whether a param is path or query - users don't need to know.

        Signature pattern:
        - Required path params: required positional/keyword args
        - Optional path params: optional keyword args (default=None)
        - All query params: keyword-only args (default=None)

        Example:
            liveGameV1(game_pk, *, timecode=None, fields=None)
        """
        # Separate path and query parameters from schema
        path_param_defs = {p["name"]: p for p in endpoint_method.path_params}
        query_param_defs = {p["name"]: p for p in endpoint_method.query_params}

        # Handle case where same param appears in both path and query
        # Remove duplicates from query_params (path takes precedence)
        query_only_params = {k: v for k, v in query_param_defs.items() if k not in path_param_defs}

        # Build signature parts
        sig_parts = []

        # Required path params first (no default)
        for param_name, param_def in path_param_defs.items():
            if param_def["required"]:
                sig_parts.append(param_name)

        # Optional path params (with default)
        for param_name, param_def in path_param_defs.items():
            if not param_def["required"]:
                sig_parts.append(f"{param_name}=None")

        # Add keyword-only separator if we have query params
        if query_only_params:
            sig_parts.append("*")

        # All query params (excluding duplicates) are keyword-only with defaults
        for param_name in query_only_params.keys():
            sig_parts.append(f"{param_name}=None")

        signature = ", ".join(sig_parts)

        # Build function body that routes args to internal path_params/query_params dicts
        path_routing = "\n".join(
            f"    if {name} is not None: path_params['{name}'] = {name}"
            for name in path_param_defs.keys()
        )
        query_routing = "\n".join(
            f"    if {name} is not None: query_params['{name}'] = {name}"
            for name in query_only_params.keys()
        )

        # Generate function using exec (captured in closure)
        func_code = f"""
def method_impl({signature}):
    # Route arguments to path_params dict
    path_params = {{}}
{path_routing}

    # Route arguments to query_params dict
    query_params = {{}}
{query_routing}

    # Execute request with routed params
    return endpoint._execute_request(
        endpoint_method=method_def,
        path_params=path_params if path_params else None,
        query_params=query_params if query_params else None,
    )
"""

        # Execute function definition with closure
        namespace = {
            "endpoint": self,
            "method_def": endpoint_method,
        }
        exec(func_code, namespace)  # nosec B102 - Safe: func_code is generated internally from schema

        return namespace["method_impl"]

    def _build_method_docstring(self, endpoint_method: EndpointMethod) -> str:
        """Build comprehensive docstring for method."""
        # Build parameter documentation with clear path/query distinction
        param_docs = []

        # Document path parameters
        if endpoint_method.path_params:
            param_docs.append("        Path Parameters (go in URL path):")
            for param in endpoint_method.path_params:
                required = "required" if param["required"] else "optional"
                param_type = param.get("type", "string")
                desc = param.get("description", "")
                param_docs.append(f"            {param['name']} ({param_type}, {required}): {desc}")

        # Document query parameters
        if endpoint_method.query_params:
            if endpoint_method.path_params:
                param_docs.append("")  # Blank line separator
            param_docs.append("        Query Parameters (go in URL query string):")
            for param in endpoint_method.query_params:
                required = "required" if param["required"] else "optional"
                param_type = param.get("type", "string")
                desc = param.get("description", "")
                param_docs.append(f"            {param['name']} ({param_type}, {required}): {desc}")

        param_section = "\n".join(param_docs) if param_docs else "        None"

        return f"""{endpoint_method.summary}

    {endpoint_method.notes}

    Path: {endpoint_method.path_template}

    Args:
{param_section}

    Returns:
        APIResponse: Response object with .json(), .save_json(), and .get_uri() methods
    """

    def _format_params_doc(self, params: list[dict]) -> str:
        """Format parameter list for docstring."""
        if not params:
            return "    None"

        lines = []
        for param in params:
            required = "required" if param["required"] else "optional"
            param_type = param.get("type", "string")
            desc = param.get("description", "")
            lines.append(f"    - {param['name']} ({param_type}, {required}): {desc}")

        return "\n".join(lines)

    def _execute_request(
        self,
        endpoint_method: EndpointMethod,
        path_params: dict | None = None,
        query_params: dict | None = None,
        attempt: int = 0,
    ) -> APIResponse:
        """
        Execute the HTTP request with retry logic.

        Args:
            endpoint_method: The method definition
            path_params: Path parameters
            query_params: Query parameters
            attempt: Current retry attempt (internal)

        Returns:
            APIResponse object

        Raises:
            Exception: If request fails after all retries
        """
        try:
            # Validate and resolve parameters
            validated_path, validated_query, resolved_path = (
                endpoint_method.validate_and_resolve_params(path_params, query_params)
            )

            # Build full URL
            url = self.BASE_URL + resolved_path
            if validated_query:
                url += "?" + urlencode(validated_query)

            # Execute request
            self.log.info(f"GET {url}")
            response = requests.get(
                url,
                headers={"Accept-Encoding": "gzip"},
                timeout=self.TIMEOUT,
            )

            # Check status
            if response.status_code != 200:
                raise AssertionError(
                    f"Request failed with status {response.status_code}: {response.text[:500]}"
                )

            # Wrap and return
            api_response = APIResponse(
                response=response,
                endpoint_name=self.endpoint_name,
                method_name=endpoint_method.method_name,
                path_params=validated_path,
                query_params=validated_query,
            )

            self.log.info(f"Success: {api_response}")
            return api_response

        except (AssertionError, requests.exceptions.RequestException) as e:
            if attempt < self.MAX_RETRIES:
                self.log.warning(
                    f"{endpoint_method}: Request failed (attempt {attempt + 1}/{self.MAX_RETRIES}): {e}"
                )
                sleep(attempt)  # Exponential backoff
                return self._execute_request(
                    endpoint_method=endpoint_method,
                    path_params=path_params,
                    query_params=query_params,
                    attempt=attempt + 1,
                )
            else:
                self.log.error(
                    f"{endpoint_method}: Request failed after {self.MAX_RETRIES} retries: {e}"
                )
                raise

    def get_method_names(self) -> list[str]:
        """Get list of available method names."""
        return list(self._methods.keys())

    def get_method(self, method_name: str) -> EndpointMethod:
        """
        Get the EndpointMethod object for introspection.

        This allows access to all schema methods like:
        - get_schema()
        - get_parameter_schema()
        - list_parameters()
        - get_long_description()

        Args:
            method_name: Name of the method

        Returns:
            EndpointMethod instance

        Raises:
            ValueError: If method not found

        Example:
            >>> method = api.Schedule.get_method("schedule")
            >>> print(method.get_long_description())
            >>> schema = method.get_schema()
            >>> param = method.get_parameter_schema("sportId")
        """
        if method_name not in self._methods:
            available = ", ".join(self.get_method_names())
            raise ValueError(
                f"Method '{method_name}' not found on {self.endpoint_name} endpoint. "
                f"Available methods: {available}"
            )

        return self._methods[method_name]

    def get_method_info(self, method_name: str) -> dict:
        """
        Get detailed information about a method.

        DEPRECATED: Use get_method() instead for full schema access.

        Args:
            method_name: Name of the method

        Returns:
            dict with method details

        Example:
            >>> info = api.Schedule.get_method_info("schedule")
            >>> print(info["path"])
            >>> print(info["summary"])
        """
        if method_name not in self._methods:
            raise ValueError(f"Method '{method_name}' not found")

        method = self._methods[method_name]
        return {
            "name": method.method_name,
            "path": method.path_template,
            "http_method": method.http_method,
            "summary": method.summary,
            "notes": method.notes,
            "path_params": method.path_params,
            "query_params": method.query_params,
        }

    def describe_method(self, method_name: str) -> str:
        """
        Get a human-readable description of a method with all its parameters.

        This is a convenience wrapper around get_method().get_long_description().

        Args:
            method_name: Name of the method

        Returns:
            str: Formatted description

        Example:
            >>> print(api.Schedule.describe_method("schedule"))
        """
        method = self.get_method(method_name)
        return method.get_long_description()

    def get_method_schema(self, method_name: str) -> dict:
        """
        Get the original schema JSON for a method.

        Args:
            method_name: Name of the method

        Returns:
            dict: Original schema definition

        Example:
            >>> schema = api.Schedule.get_method_schema("schedule")
            >>> print(schema["operation"]["parameters"])
        """
        method = self.get_method(method_name)
        return method.get_schema()
