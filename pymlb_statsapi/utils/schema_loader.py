import json
from dataclasses import dataclass
from importlib import resources

import yaml

from pymlb_statsapi.utils.env import mlb_stats_api_schema_version


@dataclass
class SchemaLoader:
    version: str = mlb_stats_api_schema_version

    @property
    def dashed_version(self):
        return self.version.replace(".", "-")

    @staticmethod
    def load_endpoint_model():
        """Load the main endpoint model schema"""
        with resources.files("pymlb_statsapi.resources.schemas") / "endpoint-model.yaml" as f:
            return yaml.safe_load(f.read_text())

    def load_api_docs(self):
        """Load API documentation"""
        filename = f"api_docs-{self.dashed_version}.json"
        with resources.files("pymlb_statsapi.resources.schemas.statsapi") / filename as f:
            return json.loads(f.read_text())

    def read_stats_schema(self, schema_name):
        """Load specific stats API schema (e.g., 'team', 'player', etc.)"""
        schema_dir = f"stats-api-{self.dashed_version}"
        filename = f"{schema_name}.json"

        with (
            resources.files(f"pymlb_statsapi.resources.schemas.statsapi.{schema_dir}")
            / filename as f
        ):
            return f.read_text()

    def load_stats_schema(self, schema_name):
        return json.loads(self.read_stats_schema(schema_name))

    def get_available_schemas(self):
        """Get list of available schema files"""
        schema_dir = f"stats-api-{self.dashed_version}"
        schema_files = resources.files(f"pymlb_statsapi.resources.schemas.statsapi.{schema_dir}")
        return [f.name for f in schema_files.iterdir() if f.name.endswith(".json")]


sl = SchemaLoader()
# Usage examples:
# my_schema_loader = SchemaLoader('1.0')
# endpoint_model = my_schema_loader.load_endpoint_model()
# team_schema = my_schema_loader.load_stats_schema('team')
# game_schema = my_schema_loader.load_stats_schema('game')
# available = my_schema_loader.get_available_schemas()
