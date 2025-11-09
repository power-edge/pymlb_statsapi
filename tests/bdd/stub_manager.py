"""
Stub manager for capturing and replaying API responses.

This allows tests to:
1. Capture real API responses as JSON stubs
2. Replay stubs for fast, deterministic testing
3. Organize stubs by endpoint and parameters
"""

import gzip
import hashlib
import json
import os
from pathlib import Path

from pymlb_statsapi.model.factory import APIResponse


class StubManager:
    """Manages API response stubs for testing."""

    def __init__(self, stub_dir: str = "tests/bdd/stubs"):
        self.stub_dir = Path(stub_dir)
        self.stub_dir.mkdir(parents=True, exist_ok=True)
        self.mode = os.environ.get("STUB_MODE", "replay")  # capture, replay, or passthrough

    def get_stub_path(
        self, endpoint: str, method: str, path_params: dict, query_params: dict
    ) -> Path:
        """
        Generate a stub file path based on request parameters.

        Format: stubs/{endpoint}/{method}/{hash}.json
        """
        # Create a deterministic hash from parameters
        param_str = json.dumps(
            {
                "path": sorted(path_params.items()) if path_params else [],
                "query": sorted(query_params.items()) if query_params else [],
            },
            sort_keys=True,
        )
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:12]

        # Create directory structure
        method_dir = self.stub_dir / endpoint / method
        method_dir.mkdir(parents=True, exist_ok=True)

        # Generate descriptive filename
        parts = [method]
        if path_params:
            parts.extend([f"{k}={v}" for k, v in sorted(path_params.items())])
        if query_params:
            parts.extend(
                [f"{k}={v}" for k, v in sorted(query_params.items())][:3]
            )  # Limit to 3 query params

        filename = "_".join(parts) + f"_{param_hash}.json"
        # Clean filename
        filename = filename.replace("/", "_").replace(":", "_")

        return method_dir / filename

    def capture_stub(self, response: APIResponse) -> Path:
        """
        Capture an API response as a stub.

        Args:
            response: The APIResponse to capture

        Returns:
            Path to the saved stub file
        """
        stub_path = self.get_stub_path(
            response.endpoint_name,
            response.method_name,
            response.path_params,
            response.query_params,
        )

        # Build stub data
        stub_data = {
            "endpoint": response.endpoint_name,
            "method": response.method_name,
            "path_params": response.path_params,
            "query_params": response.query_params,
            "url": response.url,
            "status_code": response.status_code,
            "response": response.json(),
            "path": response.get_path(),
        }

        # Save stub
        with open(stub_path, "w") as f:
            json.dump(stub_data, f, indent=2)

        print(f"Captured stub: {stub_path}")
        return stub_path

    def load_stub(
        self, endpoint: str, method: str, path_params: dict, query_params: dict
    ) -> dict | None:
        """
        Load a stub if it exists (supports both .json and .json.gz files).

        Args:
            endpoint: Endpoint name
            method: Method name
            path_params: Path parameters
            query_params: Query parameters

        Returns:
            Stub data dict or None if not found
        """
        stub_path = self.get_stub_path(endpoint, method, path_params, query_params)

        # Try gzipped version first, then regular
        gzip_path = stub_path.parent / (stub_path.name + ".gz")

        if gzip_path.exists():
            with gzip.open(gzip_path, "rt") as f:
                return json.load(f)
        elif stub_path.exists():
            with open(stub_path) as f:
                return json.load(f)
        else:
            return None

    def stub_exists(
        self, endpoint: str, method: str, path_params: dict, query_params: dict
    ) -> bool:
        """Check if a stub exists for these parameters (checks both .json and .json.gz)."""
        stub_path = self.get_stub_path(endpoint, method, path_params, query_params)
        gzip_path = stub_path.parent / (stub_path.name + ".gz")
        return stub_path.exists() or gzip_path.exists()

    def list_stubs(self, endpoint: str | None = None) -> list[Path]:
        """
        List all available stubs.

        Args:
            endpoint: Optional endpoint name to filter by

        Returns:
            List of stub file paths
        """
        if endpoint:
            search_dir = self.stub_dir / endpoint
            if not search_dir.exists():
                return []
            return list(search_dir.rglob("*.json"))
        else:
            return list(self.stub_dir.rglob("*.json"))

    def get_stub_info(self, stub_path: Path) -> dict:
        """Get information about a stub without loading full response."""
        with open(stub_path) as f:
            data = json.load(f)
        return {
            "endpoint": data["endpoint"],
            "method": data["method"],
            "path_params": data["path_params"],
            "query_params": data["query_params"],
            "url": data["url"],
            "path": data.get("path", ""),
            "stub_path": str(stub_path),
        }
