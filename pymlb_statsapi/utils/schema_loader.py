import json
import os
from dataclasses import dataclass, field
from importlib import resources
from importlib.resources import as_file


@dataclass
class SchemaLoader:
    version: str = field(default=os.environ.get("PYMLB_STATSAPI__SCHEMA_VERSION", "1.0"))

    @property
    def dashed_version(self):
        """Version with dashes for filenames (e.g., '1.0' -> '1-0')"""
        return self.version.replace(".", "-")

    @property
    def underscore_version(self):
        """Version with underscores for directory names (e.g., '1.0' -> '1_0')"""
        return self.version.replace(".", "_")

    @staticmethod
    def load_endpoint_model():
        """Load the main endpoint model schema"""
        resource = resources.files("pymlb_statsapi.resources.schemas") / "endpoint-model.json"
        with as_file(resource) as path:
            with open(path) as f:
                return json.load(f)

    def load_api_docs(self):
        """Load API documentation"""
        filename = f"api_docs-{self.dashed_version}.json"
        resource = resources.files("pymlb_statsapi.resources.schemas.statsapi") / filename
        with as_file(resource) as path:
            with open(path) as f:
                return json.load(f)

    def read_stats_schema(self, schema_name):
        """Load specific stats API schema (e.g., 'team', 'player', etc.)"""
        schema_dir = f"stats_api_{self.underscore_version}"
        filename = f"{schema_name}.json"

        resource = (
            resources.files(f"pymlb_statsapi.resources.schemas.statsapi.{schema_dir}") / filename
        )
        with as_file(resource) as path:
            with open(path) as f:
                return f.read()

    def load_stats_schema(self, schema_name):
        return json.loads(self.read_stats_schema(schema_name))

    def get_available_schemas(self):
        """Get list of available schema files"""
        schema_dir = f"stats_api_{self.underscore_version}"
        schema_files = resources.files(f"pymlb_statsapi.resources.schemas.statsapi.{schema_dir}")
        return [f.name for f in schema_files.iterdir() if f.name.endswith(".json")]


sl = SchemaLoader()
# Usage examples:
# my_schema_loader = SchemaLoader('1.0')
# endpoint_model = my_schema_loader.load_endpoint_model()
# team_schema = my_schema_loader.load_stats_schema('team')
# game_schema = my_schema_loader.load_stats_schema('game')
# available = my_schema_loader.get_available_schemas()
