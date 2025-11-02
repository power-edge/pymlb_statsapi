# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyMLB StatsAPI is a Python wrapper for MLB Stats API endpoints that enables fetching and saving MLB statistics data to any file system solution. The library is **config-driven**, with all endpoints, API methods, and parameters mapped to JSON schema files in `pymlb_statsapi/resources/`.

**NEW: Dynamic API System** - A new fully dynamic model system is available in `pymlb_statsapi/model/dynamic.py` and `dynamic_registry.py` that eliminates hardcoded model files. See `DYNAMIC_API_README.md` for details.

## Development Commands

### Environment Setup
```bash
# Python 3.13+ required
uv sync  # Install dependencies using uv package manager
```

### Code Quality
```bash
# Linting and formatting (uses ruff)
ruff check .                    # Check for linting issues
ruff check --fix .              # Auto-fix linting issues
ruff format .                   # Format code

# Pre-commit hooks (includes ruff, bandit, commitizen)
pre-commit run --all-files      # Run all pre-commit hooks
pre-commit install              # Install git hooks
```

### Testing
```bash
# Unit tests (pytest)
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest tests/unit/pymlb_statsapi/utils/test_schema_loader.py  # Run specific test

# Test dynamic API
pytest tests/unit/pymlb_statsapi/model/test_statsapi.py  # Test new dynamic system
python quick_test.py   # Quick integration test

# BDD tests (behave)
behave features/                # Run behavior-driven tests

# Run example scripts
python examples/api_example.py  # Dynamic API examples
```

### Building and Distribution
```bash
# Build package (uses hatch with vcs versioning)
hatch build                     # Build wheel and sdist
uv build                        # Alternative using uv

# Version is dynamically generated from git tags via hatch-vcs
# Version file: pymlb_statsapi/__version__.py (auto-generated)
```

## Architecture

### Core Design Pattern: Config-Driven API Wrapper

The library uses a **schema-driven approach** where MLB API endpoints are defined as JSON schemas rather than hardcoded. This enables:
- Dynamic endpoint discovery
- Self-documenting API methods
- Easy updates when MLB API changes

**Two API Implementations Available:**
1. **Original System** (`pymlb_statsapi/model/api/*.py`): Hardcoded model classes with `@configure_api` decorator
2. **Dynamic System** (`pymlb_statsapi/model/dynamic*.py`): Fully dynamic class generation from schemas - **RECOMMENDED FOR NEW CODE**

### Key Components

#### 1. Schema System (`pymlb_statsapi/resources/`)
- `endpoint-model.yaml`: Master configuration mapping endpoint names to paths and method names
- `schemas/statsapi/stats_api_1_0/*.json`: Individual endpoint schemas with full parameter definitions
- Each JSON schema defines: operations, parameters (path/query), validation rules, and documentation

#### 2. Model Layer (`pymlb_statsapi/model/`)
- **Base Models** (`base.py`):
  - `EndpointModel`: Base class for all endpoint models, parses schema JSON
  - `OperationModel`: Represents individual API operations (methods)
  - `Parameter`: Path and query parameter definitions with validation

- **API Models** (`api/*.py`):
  - One model per endpoint (e.g., `ScheduleModel`, `GameModel`, `TeamModel`)
  - Each method is decorated with `@configure_api` which:
    - Looks up path/name from `endpoint-model.yaml`
    - Returns a `StatsAPIObject` configured for that specific API call

- **Registry** (`stats_api.py`):
  - `StatsAPIModelRegistry`: Singleton that instantiates all endpoint models from schemas
  - Accessed via `StatsAPI` global: `StatsAPI.Schedule`, `StatsAPI.Game`, etc.

#### 3. Data Access (`pymlb_statsapi/utils/stats_api_object.py`)
- **`StatsAPIObject`**: The core object returned by all API methods
  - Handles HTTP requests to `statsapi.mlb.com`
  - Manages file system operations (save/load/gzip)
  - Resolves path/query parameters with validation
  - Default storage: `./.var/local/mlb_statsapi` (configurable via `PYMLB_STATSAPI__BASE_FILE_PATH`)

- **Key Methods**:
  - `.get()`: Fetch data from API with retry logic
  - `.save()`: Save JSON to file system
  - `.gzip()`: Save as gzipped JSON
  - `.load()`: Load previously saved data

#### 4. Schema Loader (`pymlb_statsapi/utils/schema_loader.py`)
- `SchemaLoader`: Handles loading schemas from packaged resources
- Uses `importlib.resources` for proper package resource access
- Version-aware: defaults to version 1.0 but supports multiple versions

### Data Flow Example

```python
# User code
from pymlb_statsapi.model import StatsAPI
sch = StatsAPI.Schedule.schedule(query_params={"sportId": 1, "date": "2025-06-01"})

# Behind the scenes:
# 1. StatsAPI.Schedule -> ScheduleModel instance (loaded from schedule.json schema)
# 2. .schedule() -> @configure_api decorator looks up "schedule" in endpoint-model.yaml
# 3. Returns StatsAPIObject with:
#    - endpoint: ScheduleModel
#    - api: specific API definition from schema
#    - operation: the GET operation with parameter rules
#    - Resolved URL: https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-06-01

# 4. User calls sch.get() -> HTTP request + validation
# 5. User calls sch.gzip() -> Save to file system
```

### Important Implementation Details

- **Parameter Resolution** (`resolve_path` in `stats_api_object.py`):
  - Path params substitute into URL path (e.g., `/v1/game/{game_pk}`)
  - Query params append as query string with validation
  - Enforces required params, enums, and allowMultiple rules

- **Decorator Pattern** (`@configure_api`):
  - Maps method names to schema definitions
  - Handles misnaming between code and beta API docs
  - Centralizes endpoint configuration in YAML

- **Singleton Pattern**: Used in `EndpointConfig` and model registry for efficient schema loading

### Dynamic API System (NEW - Recommended)

The new dynamic system (`pymlb_statsapi/model/dynamic.py` and `dynamic_registry.py`) eliminates all hardcoding:

#### Key Components:

1. **`DynamicStatsAPI`**: Registry that auto-generates endpoint classes from JSON schemas
   - No manual class definitions needed
   - Automatically discovers all schemas in `resources/schemas/statsapi/stats_api_1_0/`
   - Methods generated from schema operations

2. **`DynamicEndpoint`**: Dynamically generated endpoint class
   - Methods created at runtime from schema definitions
   - Built-in parameter validation from schemas
   - Configurable method exclusions for broken endpoints

3. **`APIResponse`**: Enhanced response wrapper
   - Wraps `requests.Response` with metadata
   - `.json()` returns parsed data (copyright auto-removed)
   - Includes URL metadata: `domain`, `path`, `query_params`, `path_params`

4. **`EndpointMethod`**: Represents a single API method
   - Schema-based parameter validation
   - URL resolution with path/query param substitution
   - Enum and type validation

#### Usage Example:

```python
from pymlb_statsapi.model.registry import StatsAPI

# Make request (auto-fetches, no .get() call needed)
response = StatsAPI.Schedule.schedule(query_params={
    "sportId": 1,
    "date": "2025-06-01"
})

# Access data
data = response.json()

# Save to file
result = response.gzip(...)
```

#### Key Differences from Original System:

| Feature | Original | Dynamic |
|---------|----------|---------|
| Model files | Manual classes | Auto-generated |
| Method definitions | Hardcoded | From schemas |
| Response | `StatsAPIObject` | `APIResponse` |
| Data access | `.get()` then `.obj` | `.json()` directly |
| Updates | Edit Python files | Update JSON schemas |
| Method exclusions | `raise NotImplementedError` | Config-based |

#### Method Exclusions:

Configure broken endpoints in `EXCLUDED_METHODS` in `dynamic_registry.py`:

```python
EXCLUDED_METHODS = {
    "team": {"affiliates", "allTeams"},  # Known broken in beta API
}
```

For complete documentation, see:
- `DYNAMIC_API_README.md` - Architecture and overview
- `pymlb_statsapi/model/API_USAGE.md` - Usage guide with examples
- `examples/dynamic_api_example.py` - Working code examples
- `tests/unit/pymlb_statsapi/model/test_dynamic.py` - Test examples

## Configuration Files

- **`pyproject.toml`**: Project metadata, dependencies, tool configurations
  - Uses `hatch` build backend with `hatch-vcs` for git-based versioning
  - Ruff config: line length 100, Python 3.13 target
  - Pytest config with strict markers

- **`.pre-commit-config.yaml`**: Git hooks for code quality
  - Ruff (lint + format)
  - Bandit (security)
  - Commitizen (conventional commits)

## Environment Variables

- `PYMLB_STATSAPI__BASE_FILE_PATH`: Base directory for saving API responses (default: `./.var/local/mlb_statsapi`)
- `PYMLB_STATSAPI__BASE_FILE_PATH`: Max retry attempts for API requests (default: 3) [Note: This appears to be reused incorrectly in code]

## Adding New Endpoints

1. Obtain JSON schema from MLB Stats API docs
2. Place in `pymlb_statsapi/resources/schemas/statsapi/stats_api_1_0/{endpoint_name}.json`
3. Add endpoint configuration to `endpoint-model.yaml`
4. Create model class in `pymlb_statsapi/model/api/{endpoint_name}.py`:
   - Inherit from `EndpointModel`
   - Add methods decorated with `@configure_api`
5. Register in `StatsAPIModelRegistry` (`stats_api.py`)
6. Add imports to `pymlb_statsapi/model/__init__.py`

## Dependencies

**Core**:
- `requests`: HTTP client for API calls
- `serde`: Serialization/deserialization for models
- `pyyaml`: YAML config parsing

**Dev**:
- `hatch`: Build backend and versioning
- `ruff`: Linting and formatting
- `pytest`: Unit testing
- `behave`: BDD testing
- `pre-commit`: Git hooks
- `bandit`: Security scanning
