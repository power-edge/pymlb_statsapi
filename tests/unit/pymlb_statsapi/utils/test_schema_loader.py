import json
import yaml
from functools import wraps
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pymlb_statsapi.utils.schema_loader import SchemaLoader


def parameterize_versions(versions):
    """Custom decorator to parameterize tests by versions."""

    def decorator(test_func):
        @wraps(test_func)
        def wrapper(self, *args, **kwargs):
            for version in versions:
                with self.subTest(version=version):
                    test_func(self, version, *args, **kwargs)

        return wrapper

    return decorator


class TestSchemaLoader(TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.default_version = "1.0"
        self.schema_loader = SchemaLoader(version=self.default_version)

        # Sample test data
        self.sample_endpoint_model = {
            "endpoints": {
                "/api/v1/teams": {
                    "method": "GET",
                    "description": "Get teams"
                }
            }
        }

        self.sample_api_docs = {
            "info": {
                "title": "MLB Stats API",
                "version": "1.0"
            },
            "paths": {}
        }

        self.sample_team_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        }

    # def test_initialization_default_version(self):
    #     """Test SchemaLoader initialization with default version."""
    #     with patch('pymlb_statsapi.utils.schema_loader.mlb_stats_api_schema_version', '2.0'):
    #         loader = SchemaLoader()
    #         self.assertEqual(loader.version, '2.0')

    @parameterize_versions([
        "1.0",
        # "2.0", "3.0"
    ])
    def test_initialization_custom_version(self, version):
        """Test SchemaLoader initialization with custom version."""
        loader = SchemaLoader(version=version)
        self.assertEqual(loader.version, version)

    @parameterize_versions([
        "1.0",
        # "2.0", "3.0"
    ])
    def test_dashed_version_property(self, version):
        """Test dashed_version property converts dots to dashes."""
        loader = SchemaLoader(version=version)
        expected = version.replace('.', '-')
        self.assertEqual(loader.dashed_version, expected)

    def test_dashed_version_property_complex(self):
        """Test dashed_version with more complex version strings."""
        test_cases = [
            ("1.0.1", "1-0-1"),
            ("2.1.3", "2-1-3"),
            ("1.0.0-beta", "1-0-0-beta"),
            ("1.0", "1-0")
        ]

        for version, expected in test_cases:
            with self.subTest(version=version):
                loader = SchemaLoader(version=version)
                self.assertEqual(loader.dashed_version, expected)

    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    @patch('pymlb_statsapi.utils.schema_loader.yaml.safe_load')
    def test_load_endpoint_model_success(self, mock_yaml_load, mock_files):
        """Test successful loading of endpoint model."""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.read_text.return_value = "test yaml content"
        mock_files.return_value.__truediv__.return_value = mock_file
        mock_yaml_load.return_value = self.sample_endpoint_model

        result = SchemaLoader.load_endpoint_model()

        # Assertions
        mock_files.assert_called_once_with("pymlb_statsapi.resources.schemas")
        # mock_file.read_text.assert_called_once()
        # mock_yaml_load.assert_called_once_with("test yaml content")
        self.assertEqual(result, self.sample_endpoint_model)

    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_load_endpoint_model_file_not_found(self, mock_files):
        """Test load_endpoint_model when file is not found."""
        mock_files.return_value.__truediv__.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FileNotFoundError):
            SchemaLoader.load_endpoint_model()

    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    @patch('pymlb_statsapi.utils.schema_loader.yaml.safe_load')
    def test_load_endpoint_model_yaml_error(self, mock_yaml_load, mock_files):
        """Test load_endpoint_model when YAML parsing fails."""
        mock_file = MagicMock()
        mock_file.read_text.return_value = "invalid yaml content"
        mock_files.return_value.__truediv__.return_value = mock_file
        mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")

        with self.assertRaises(yaml.YAMLError):
            SchemaLoader.load_endpoint_model()

    @parameterize_versions([
        "1.0",
        # "2.0"
    ])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    @patch('pymlb_statsapi.utils.schema_loader.json.loads')
    def test_load_api_docs_success(self, version, mock_json_loads, mock_files):
        """Test successful loading of API docs."""
        loader = SchemaLoader(version=version)
        expected_filename = f"api_docs-{version.replace('.', '-')}.json"

        # Setup mocks
        mock_file = MagicMock()
        mock_file.read_text.return_value = '{"test": "content"}'
        mock_files.return_value.__truediv__.return_value = mock_file
        mock_json_loads.return_value = self.sample_api_docs

        result = loader.load_api_docs()

        # Assertions
        mock_files.assert_called_once_with("pymlb_statsapi.resources.schemas.statsapi")
        mock_files.return_value.__truediv__.assert_called_once_with(expected_filename)
        # mock_file.read_text.assert_called_once()  # Ensure read_text is called
        # mock_json_loads.assert_called_once_with('{"test": "content"}')
        self.assertEqual(result, self.sample_api_docs)

    @parameterize_versions(["1.0"])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_load_api_docs_file_not_found(self, version, mock_files):
        """Test load_api_docs when file is not found."""
        loader = SchemaLoader(version=version)
        mock_files.return_value.__truediv__.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FileNotFoundError):
            loader.load_api_docs()

    @parameterize_versions([
        "1.0",
        # "2.0"
    ])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_read_stats_schema_success(self, version, mock_files):
        """Test successful reading of stats schema."""
        loader = SchemaLoader(version=version)
        schema_name = "team"
        expected_dir = f"pymlb_statsapi.resources.schemas.statsapi.stats-api-{version.replace('.', '-')}"
        expected_filename = f"{schema_name}.json"

        # Setup mocks
        mock_file = MagicMock()
        mock_file.read_text.return_value = '{"test": "schema"}'
        mock_files.return_value.__truediv__.return_value = mock_file

        result = loader.read_stats_schema(schema_name)

        # Assertions
        mock_files.assert_called_once_with(expected_dir)
        mock_files.return_value.__truediv__.assert_called_once_with(expected_filename)
        # mock_file.read_text.assert_called_once()
        # self.assertEqual(result, '{"test": "schema"}')

    @parameterize_versions(["1.0"])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_read_stats_schema_file_not_found(self, version, mock_files):
        """Test read_stats_schema when file is not found."""
        loader = SchemaLoader(version=version)
        mock_files.return_value.__truediv__.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FileNotFoundError):
            loader.read_stats_schema("team")

    @parameterize_versions([
        "1.0",
        # "2.0"
    ])
    @patch.object(SchemaLoader, 'read_stats_schema')
    @patch('pymlb_statsapi.utils.schema_loader.json.loads')
    def test_load_stats_schema_success(self, version, mock_json_loads, mock_read_schema):
        """Test successful loading and parsing of stats schema."""
        loader = SchemaLoader(version=version)
        schema_name = "team"

        # Setup mocks
        mock_read_schema.return_value = '{"test": "schema"}'
        mock_json_loads.return_value = self.sample_team_schema

        result = loader.load_stats_schema(schema_name)

        # Assertions
        mock_read_schema.assert_called_once_with(schema_name)
        mock_json_loads.assert_called_once_with('{"test": "schema"}')
        self.assertEqual(result, self.sample_team_schema)

    @parameterize_versions(["1.0"])
    @patch.object(SchemaLoader, 'read_stats_schema')
    @patch('pymlb_statsapi.utils.schema_loader.json.loads')
    def test_load_stats_schema_json_error(self, version, mock_json_loads, mock_read_schema):
        """Test load_stats_schema when JSON parsing fails."""
        loader = SchemaLoader(version=version)

        mock_read_schema.return_value = 'invalid json'
        mock_json_loads.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        with self.assertRaises(json.JSONDecodeError):
            loader.load_stats_schema("team")

    @parameterize_versions(["1.0", "2.0"])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_get_available_schemas_success(self, version, mock_files):
        """Test successful retrieval of available schemas."""
        loader = SchemaLoader(version=version)
        expected_dir = f"pymlb_statsapi.resources.schemas.statsapi.stats-api-{version.replace('.', '-')}"

        # Setup mock directory with files
        mock_file1 = MagicMock()
        mock_file1.name = "team.json"
        mock_file2 = MagicMock()
        mock_file2.name = "player.json"
        mock_file3 = MagicMock()
        mock_file3.name = "__init__.py"  # Should be filtered out
        mock_file4 = MagicMock()
        mock_file4.name = "game.json"

        mock_schema_files = MagicMock()
        mock_schema_files.iterdir.return_value = [mock_file1, mock_file2, mock_file3, mock_file4]
        mock_files.return_value = mock_schema_files

        result = loader.get_available_schemas()

        # Assertions
        mock_files.assert_called_once_with(expected_dir)
        mock_schema_files.iterdir.assert_called_once()
        expected_schemas = ["team.json", "player.json", "game.json"]
        self.assertEqual(sorted(result), sorted(expected_schemas))

    @parameterize_versions(["1.0"])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_get_available_schemas_empty_directory(self, version, mock_files):
        """Test get_available_schemas with empty directory."""
        loader = SchemaLoader(version=version)

        mock_schema_files = MagicMock()
        mock_schema_files.iterdir.return_value = []
        mock_files.return_value = mock_schema_files

        result = loader.get_available_schemas()

        self.assertEqual(result, [])

    @parameterize_versions(["1.0"])
    @patch('pymlb_statsapi.utils.schema_loader.resources.files')
    def test_get_available_schemas_directory_not_found(self, version, mock_files):
        """Test get_available_schemas when directory is not found."""
        loader = SchemaLoader(version=version)
        mock_files.side_effect = FileNotFoundError("Directory not found")

        with self.assertRaises(FileNotFoundError):
            loader.get_available_schemas()

    def test_multiple_schema_operations(self):
        """Integration test for multiple schema operations."""
        with patch('pymlb_statsapi.utils.schema_loader.resources.files') as mock_files, \
                patch('pymlb_statsapi.utils.schema_loader.json.loads') as mock_json_loads, \
                patch.object(SchemaLoader, 'read_stats_schema') as mock_read_schema:
            loader = SchemaLoader(version="1.0")

            # Setup mocks for different operations
            mock_file = MagicMock()
            mock_file.read_text.return_value = '{"test": "api_docs"}'
            mock_files.return_value.__truediv__.return_value = mock_file
            mock_json_loads.return_value = self.sample_api_docs
            mock_read_schema.return_value = '{"test": "team_schema"}'

            # Test multiple operations
            api_docs = loader.load_api_docs()
            team_schema_text = loader.read_stats_schema("team")

            # Assertions
            self.assertEqual(api_docs, self.sample_api_docs)
            self.assertEqual(team_schema_text, '{"test": "team_schema"}')

    def test_edge_cases_schema_names(self):
        """Test edge cases for schema names."""
        with patch.object(SchemaLoader, 'read_stats_schema') as mock_read_schema:
            loader = SchemaLoader(version="1.0")

            # Test various schema name formats
            test_cases = [
                "team",
                "team-stats",
                "player_info",
                "game.detail"  # This might be unusual but should work
            ]

            mock_read_schema.return_value = '{"test": "schema"}'

            for schema_name in test_cases:
                with self.subTest(schema_name=schema_name):
                    result = loader.read_stats_schema(schema_name)
                    mock_read_schema.assert_called_with(schema_name)
                    self.assertEqual(result, '{"test": "schema"}')