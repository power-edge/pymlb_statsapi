# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working with this repository.

## Project Overview

PyMLB StatsAPI is a fully **schema-driven** Python wrapper for the MLB Stats API. All endpoints, methods, and parameters are dynamically generated from JSON schemas - there are no hardcoded model classes.

### Key Features
- **100% Schema-Driven**: Endpoints and methods generated dynamically from JSON schemas
- **Zero Hardcoding**: No manual class definitions needed
- **Storage Optimized**: All test stubs gzipped (80-95% size reduction)
- **Type-Safe**: Full parameter validation from schemas
- **Well-Tested**: 39/39 BDD scenarios passing with stubbed responses
- **Timestamped**: All saved data includes capture timestamp for reference

## Quick Start

```bash
# Setup
uv sync

# Run tests
uv run pytest                          # Unit tests
uv run behave tests/bdd/              # BDD tests (with stubs)

# Code quality
ruff check --fix .                     # Lint and auto-fix
ruff format .                          # Format code
pre-commit run --all-files             # Run all hooks

# Git workflow helper (interactive)
bash scripts/git.sh                    # Format, commit, release, push
```

## Development Workflow

### Git Workflow Script

The `scripts/git.sh` helper script provides an interactive menu for common git operations:

1. **Format & commit changes** - Runs ruff format/check, then commits
2. **Create release** - Bump version (patch/minor/major) and create git tag
3. **Push to remote** - Push commits and optionally tags
4. **Full release** - Complete workflow: format, commit, bump, tag, push, build
5. **Status** - Show current git status

**Usage:**
```bash
bash scripts/git.sh                    # Interactive menu
./scripts/git.sh commit "feat: message"  # Direct command
./scripts/git.sh release minor         # Bump minor version
./scripts/git.sh full 1.0.0            # Full release workflow
```

### CI/CD Checks

For full validation before pushing, reference `.github/workflows/test.yml` which runs:

**Test Job** (matrix: Python 3.11/3.12/3.13 on Ubuntu/macOS/Windows):
- `ruff check .` - Linting
- `ruff format --check .` - Format verification
- `mypy pymlb_statsapi/` - Type checking (continue-on-error)
- `bandit -r pymlb_statsapi/ -ll` - Security scanning
- `pytest --cov` - Unit tests with coverage
- `STUB_MODE=replay behave` - BDD tests with stubs

**Build Job:**
- `uv build` - Build wheel and sdist
- `twine check dist/*` - Validate package

**Docs Job:**
- `make html` - Build Sphinx documentation

To run the full CI suite locally:
```bash
# Linting and security
ruff check .
ruff format --check .
bandit -r pymlb_statsapi/ -ll

# Tests
pytest --cov=pymlb_statsapi --cov-report=term-missing
STUB_MODE=replay uv run behave

# Build
uv build
```

## Architecture

### Schema-Driven Design

Everything is driven by JSON schemas in `pymlb_statsapi/resources/schemas/statsapi/stats_api_1_0/`:

```
schedule.json → DynamicEndpoint("schedule") → schedule.schedule(date="2024-10-27")
game.json     → DynamicEndpoint("game")     → game.boxscore(game_pk="747175")
person.json   → DynamicEndpoint("person")   → person.person(personIds="660271")
```

### Core Components

#### 1. `pymlb_statsapi/model/factory.py`

**`APIResponse`**: Response wrapper returned by all API calls
- `.json()` - Get parsed response data
- `.gzip(prefix="data")` - Save as gzipped JSON with metadata and timestamp
- `.save_json(prefix="data", gzip=True)` - Alternative save method
- `.get_uri(prefix="data", gzip=True)` - Get file:// URI
- `.get_metadata()` - Get request/response metadata including timestamp

**`EndpointMethod`**: Represents a single API method
- `.get_schema()` - Get original JSON schema
- `.get_parameter_schema("sportId")` - Get parameter definition
- `.list_parameters()` - List all path/query parameters
- `.get_long_description()` - Formatted documentation

**`Endpoint`**: Dynamically generated endpoint class
- Methods created at runtime from schemas
- Built-in parameter validation
- Automatic retry logic with exponential backoff

#### 2. `pymlb_statsapi/model/registry.py`

**`StatsAPI`**: Global registry providing access to all endpoints
- Auto-discovers schemas in resources directory
- Lazy-loads endpoints for performance
- Configurable method exclusions

```python
from pymlb_statsapi import api

# Access any endpoint
api.Schedule.schedule(sportId=1, date="2024-10-27")
api.Game.boxscore(game_pk="747175")
api.Person.person(personIds="660271")
```

#### 3. `pymlb_statsapi/utils/schema_loader.py`

**`SchemaLoader`**: Handles loading JSON schemas from package resources
- Uses `importlib.resources` for proper package access
- Version-aware (defaults to v1.0)
- Caches schemas for performance

### Data Flow

```python
# 1. User calls method
response = api.Schedule.schedule(sportId=1, date="2024-10-27")

# 2. Behind the scenes:
#    - registry.py: Get/create Schedule endpoint
#    - factory.py: Endpoint.__init__ generates method from schedule.json
#    - factory.py: Method validates parameters from schema
#    - factory.py: HTTP GET with retry logic
#    - factory.py: Return APIResponse wrapper with timestamp

# 3. User accesses data
data = response.json()
result = response.gzip(prefix="mlb-data")  # Save gzipped with metadata
print(f"Captured at: {result['timestamp']}")
```

### Saved Data Format

All saved files include metadata wrapper with timestamp:

```json
{
  "metadata": {
    "request": {
      "endpoint_name": "schedule",
      "method_name": "schedule",
      "path_params": {},
      "query_params": {"sportId": "1", "date": "2024-10-27"},
      "url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-10-27",
      "timestamp": "2025-01-15T10:30:00.123456+00:00"
    },
    "response": {
      "status_code": 200,
      "elapsed_ms": 245.3
    }
  },
  "data": {
    "dates": [...]
  }
}
```

## Testing Strategy

### BDD Tests (`tests/bdd/`)

Tests use **stub capture/replay** for fast, deterministic testing:

```bash
# Capture stubs (makes real API calls)
STUB_MODE=capture uv run behave tests/bdd/game.feature

# Replay from stubs (fast, no API calls)
STUB_MODE=replay uv run behave tests/bdd/    # default mode

# Run specific schema or method
uv run behave tests/bdd/ --tags=@schema:Game
uv run behave tests/bdd/ --tags=@method:boxscore
```

#### Stub Infrastructure

- **`tests/bdd/stub_manager.py`**: Handles stub capture/replay
- **`tests/bdd/stubs/`**: All stubs stored as gzipped JSON (`.json.gz`)
- **Stub format**:
  ```json
  {
    "endpoint": "game",
    "method": "boxscore",
    "path_params": {"game_pk": "747175"},
    "query_params": {},
    "url": "https://statsapi.mlb.com/api/v1/game/747175/boxscore",
    "status_code": 200,
    "response": {...}
  }
  ```

#### Test Data Strategy

- Use **completed games** from past seasons (data won't change)
- Example: World Series 2024 games (`game_pk=747175`, `game_pk=747176`)
- Stable dates: October 2024 for schedules
- All stubs gzipped for efficient CI/CD storage

### Unit Tests (`tests/unit/`)

Traditional pytest unit tests for:
- Schema loading
- Parameter validation
- Method generation
- Utility functions

## Storage Configuration

All responses save to **file-only storage** (gzipped by default with metadata):

```python
# Save response with metadata and timestamp
response = api.Schedule.schedule(sportId=1, date="2024-10-27")
result = response.gzip(prefix="mlb-data")

# Result includes:
# - path: Full file path
# - bytes_written: Size of compressed file
# - timestamp: ISO 8601 UTC timestamp of API call
# - uri: ParseResult with file:// URI

# Generates path:
# $PYMLB_STATSAPI__BASE_FILE_PATH/mlb-data/schedule/schedule/date=2024-10-27&sportId=1.json.gz

# Default base path: ./.var/local/mlb_statsapi
# Override with: export PYMLB_STATSAPI__BASE_FILE_PATH=/path/to/data
```

## Configuration Files

### `pyproject.toml`
- **Build**: hatch + hatch-vcs (git-based versioning)
- **Lint/Format**: ruff (line length 100, Python 3.13)
- **Test**: pytest with strict markers
- **Security**: bandit configuration

### `.pre-commit-config.yaml`
Pre-commit hooks ensure code quality:
- **ruff**: Lint and format
- **bandit**: Security scanning (excludes test stubs)
- **commitizen**: Conventional commits

### `behave.ini`
BDD test configuration:
- Test path: `tests/bdd/`
- Report path: `reports/`
- Output format options

## Environment Variables

- `PYMLB_STATSAPI__BASE_FILE_PATH`: Base directory for file storage (default: `./.var/local/mlb_statsapi`)
- `PYMLB_STATSAPI__MAX_RETRIES`: Max retry attempts (default: 3)
- `PYMLB_STATSAPI__TIMEOUT`: Request timeout in seconds (default: 30)
- `STUB_MODE`: Test stub mode (`capture`, `replay`, `passthrough`)

## Adding New Endpoints

When MLB adds new endpoints:

1. **Get JSON schema** from MLB Stats API documentation
2. **Add to resources**: `pymlb_statsapi/resources/schemas/statsapi/stats_api_1_0/{endpoint}.json`
3. **Restart app**: Dynamic registry auto-discovers new schemas
4. **Create tests**: Add BDD tests in `tests/bdd/{endpoint}.feature`
5. **Capture stubs**: `STUB_MODE=capture uv run behave tests/bdd/{endpoint}.feature`

That's it! No code changes needed - the system is fully schema-driven.

## Development Workflow

### Making Changes

1. **Branch**: Work on feature branches
2. **Test**: Run BDD and unit tests
3. **Lint**: `ruff check --fix . && ruff format .`
4. **Commit**: Use conventional commits (`feat:`, `fix:`, `refactor:`, etc.)
5. **Pre-commit**: Hooks run automatically

### Git Operations

Use `scripts/git.sh` for streamlined git operations:

```bash
# Interactive mode
bash scripts/git.sh

# CLI mode
bash scripts/git.sh status
bash scripts/git.sh commit "feat: add new feature"
bash scripts/git.sh push
bash scripts/git.sh full    # format, commit, push, build
```

### Release Process

Version is automatically generated from git tags (hatch-vcs):

```bash
# Commit all changes
bash scripts/git.sh commit "feat: ..."

# Push to trigger CI/CD
bash scripts/git.sh push

# Version will be: {last_tag}.dev{commits_since}+{short_hash}
```

## Common Tasks

### Capture New Test Stubs

```bash
# Capture stubs for specific endpoint
STUB_MODE=capture uv run behave tests/bdd/game.feature

# Capture all stubs (be patient, rate-limited)
STUB_MODE=capture uv run behave tests/bdd/
```

### Run Selective Tests

```bash
# By schema
uv run behave tests/bdd/ --tags=@schema:Game

# By method
uv run behave tests/bdd/ --tags=@method:liveGameV1

# Combined
uv run behave tests/bdd/ --tags=@schema:Game --tags=@method:boxscore
```

### Verify Documentation

```bash
# Validate all code examples in docs
python scripts/verify_docs_examples.py

# Validate setup for release
python scripts/validate_setup.py
```

### Build Package

```bash
# Build wheel and sdist
uv build

# Install locally for testing
uv pip install -e .
```

## Code Style Guidelines

### Parameter Naming

- **IMPORTANT**: Preserve exact parameter names from schemas
- Do NOT convert camelCase to snake_case
- Keep `sportId`, not `sport_id`
- Keep `game_pk`, not `game_id`

### Docstrings

- Use schema summary/notes for method docstrings
- Document path vs query parameters clearly
- Include examples with actual parameter values
- Show gzip usage in examples

### Testing

- BDD tests for API integration (with stubs)
- Unit tests for internal logic
- Use completed games for stable test data
- Tag all scenarios with `@schema:` and `@method:`
- Always gzip test stubs

## Troubleshooting

### Tests Failing

```bash
# Check if stubs exist
ls tests/bdd/stubs/{endpoint}/{method}/

# Recapture stubs
STUB_MODE=capture uv run behave tests/bdd/{endpoint}.feature

# Check stub format (should have no cache_key)
python -c "import gzip, json; print(json.load(gzip.open('path/to/stub.json.gz')))"
```

### Import Errors

```bash
# Reinstall in editable mode
uv pip install -e .

# Check package structure
python -c "from pymlb_statsapi import api; print(api.get_endpoint_names())"
```

### Pre-commit Issues

```bash
# Run hooks manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Skip hooks (emergency only)
git commit --no-verify
```

## Key Principles

1. **Schema is Truth**: JSON schemas define everything
2. **No Hardcoding**: Generate, don't write
3. **Gzip Everything**: Storage efficiency matters
4. **Always Timestamp**: Track when data was captured
5. **Test with Stubs**: Fast, deterministic, offline-capable
6. **Conventional Commits**: Clear history, automatic changelogs

## Resources

- **Documentation**: `docs/` (Sphinx RST format)
- **Examples**: `examples/` (working code examples)
- **Schemas**: `pymlb_statsapi/resources/schemas/`
- **Tests**: `tests/bdd/` and `tests/unit/`
- **Scripts**: `scripts/` (git, validation, documentation)

## Current Status

✅ **Production Ready (v1.0.0)**
- All 39/39 BDD scenarios passing
- All unit tests passing
- All pre-commit hooks passing
- Documentation complete and up-to-date
- Storage simplified (file-only, gzip by default)
- Repository optimized (all stubs compressed)
- All saved data includes timestamps

Ready for release!
