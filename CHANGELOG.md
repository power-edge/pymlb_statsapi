# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-30

### 🎉 Initial Release

Production-ready Python wrapper for the MLB Stats API with clean, Pythonic interface and comprehensive schema introspection.

### Features

#### Clean Pythonic API
- Direct parameter passing - parameters are function arguments, not dicts
- Automatic parameter routing from schema (path vs query handled internally)
- Preserved parameter names match MLB Stats API exactly (e.g., `sportId`, `teamId`)
- Method overloading with automatic variant selection
- Type-safe parameter validation from schemas

#### Schema Introspection
- Access original JSON schemas programmatically
- Discover available parameters without external docs
- Get detailed parameter information including types, descriptions, and requirements
- Generate human-readable documentation from schemas
- Build tools and validators from schema definitions

#### Comprehensive Testing
- 39 BDD test scenarios covering all major endpoints
- Stub capture and replay system for fast, deterministic testing
- Multi-platform support (Ubuntu, macOS, Windows)
- Python 3.11, 3.12, 3.13 compatible

#### Developer Experience
- Fully documented with examples
- GitHub Actions CI/CD pipeline
- Code coverage reporting
- ReadTheDocs integration
- Makefile for common tasks
- Pre-commit hooks for code quality

#### Endpoints Supported
- Schedule (games, postseason, tied games)
- Game (live feed, boxscore, play-by-play, linescore, content)
- Team (rosters, stats, coaches, alumni)
- Person (player info, stats, awards)
- Season (all seasons, specific season data)
- Stats (hitting, pitching, fielding by group)
- League, Division, Sports (reference data)

### Usage

```python
from pymlb_statsapi import api

# Get schedule
response = api.Schedule.schedule(sportId=1, date="2025-06-01")
data = response.json()

# Get live game data
response = api.Game.liveGameV1(game_pk="747175")
data = response.json()

# Discover parameters
method = api.Schedule.get_method("schedule")
params = method.list_parameters()
```

### Requirements

- Python 3.11 or higher
- requests library

### Links

- [Documentation](https://pymlb-statsapi.readthedocs.io/)
- [PyPI Package](https://pypi.org/project/pymlb-statsapi/)
- [GitHub Repository](https://github.com/power-edge/pymlb_statsapi)
- [Issue Tracker](https://github.com/power-edge/pymlb_statsapi/issues)

---

## Development History

This section documents the evolution of the library during the pre-1.0 development phase.

### Phase 3: Clean API Refactor & Testing Infrastructure (January 2025)

#### Clean API Implementation
- **Eliminated dict-based parameter passing**: Parameters are now function arguments, not dicts
- **Automatic parameter routing**: Schema-driven path vs query parameter handling
- **Preserved MLB API parameter names**: No conversion to snake_case (e.g., `sportId`, not `sport_id`)
- **Method overloading support**: Automatic variant selection based on path parameters
- **Type-safe validation**: All validation from JSON schemas

**Before:**
```python
api.Game.liveGameV1(
    path_params={"game_pk": "747175"},
    query_params={"timecode": "20241027_000000"}
)
```

**After:**
```python
api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
```

#### Testing & Quality
- **39 BDD test scenarios** covering all major endpoints
- **Stub capture/replay system** for fast, deterministic testing
- **Multi-platform CI/CD** via GitHub Actions (Ubuntu, macOS, Windows)
- **Code quality tools**: Ruff linting, Bandit security, pre-commit hooks
- **Coverage reporting** via Codecov
- **ReadTheDocs integration** for automated documentation

#### Documentation
- Comprehensive README with badges and examples
- API usage guides and architecture documentation
- BDD testing guide in `features/README.md`
- Makefile for common development tasks
- GitHub workflows for automated testing

### Phase 2: Schema Introspection (December 2024)

#### Schema Access Methods
Added powerful introspection capabilities to discover API structure programmatically:

**EndpointMethod Methods:**
- `get_schema()` - Get complete original JSON schema
- `get_parameter_schema(param_name)` - Get specific parameter details
- `list_parameters()` - List all parameters organized by path/query
- `get_long_description()` - Human-readable formatted descriptions

**Endpoint Methods:**
- `get_method(method_name)` - Get EndpointMethod for introspection
- `describe_method(method_name)` - Get formatted description
- `get_method_schema(method_name)` - Get original schema JSON

#### Use Cases Enabled
- **Self-documentation**: No external API docs needed
- **IDE integration**: Foundation for type hints and autocomplete
- **Debugging**: Inspect schemas when API calls fail
- **Validation**: Check parameters before making requests
- **Doc generation**: Auto-generate API documentation from schemas
- **Tool building**: Build CLIs, GUIs, or other interfaces programmatically
- **Testing**: Generate test cases from schemas

**Example:**
```python
# Discover API without external docs
method = api.Schedule.get_method("schedule")
print(method.get_long_description())

# Check parameter details
param = method.get_parameter_schema("sportId")
print(f"Type: {param['type']}, Required: {param['required']}")

# List all parameters
params = method.list_parameters()
for p in params["query"]:
    print(f"{p['name']}: {p['description']}")
```

### Phase 1: Dynamic Model System (November 2024)

#### Core Architecture
Created fully dynamic model system that eliminates hardcoded endpoint classes:

**Key Components:**
- `APIResponse` - Response wrapper with metadata
- `EndpointMethod` - Method representation with schema-based validation
- `DynamicEndpoint` - Dynamically generated endpoint classes
- `DynamicStatsAPI` - Registry with automatic schema discovery

**Benefits:**
- Zero hardcoded model files needed
- All endpoints/methods auto-generated from schemas
- Config-based method exclusions
- Direct data access via `.json()`
- Method overloading with intelligent routing

#### Method Overloading
Automatic handling of MLB API endpoints with multiple variants:

```python
# seasons() has 2 variants:
# 1. GET /v1/seasons (list all)
# 2. GET /v1/seasons/{seasonId} (get specific)

# Call without path params → variant 1
all_seasons = api.Season.seasons()

# Call with seasonId → variant 2
season_2024 = api.Season.seasons(path_params={"seasonId": "2024"})
```

Other overloaded methods:
- `Schedule.schedule()` - base and scheduleType variants
- `Person.currentGameStats()` - base, personId, and personId+gamePk variants
- `League.allStarFinalVote()`, `League.allStarWriteIns()` - leagueId variants

#### Configuration System
- **Environment variables**: `PYMLB_STATSAPI__MAX_RETRIES`, `PYMLB_STATSAPI__TIMEOUT`
- **Method exclusions**: Config-based via `EXCLUDED_METHODS` dict
- **Schema versioning**: Support for multiple API versions

#### Performance
- **Initialization**: ~100ms to load all 21 endpoints (one-time)
- **Method calls**: Same as direct HTTP (no overhead)
- **Memory**: Minimal overhead (~1MB for all endpoint definitions)

### Phase 0: Foundation (October 2024)

#### Initial Implementation
- Schema-driven architecture with JSON schemas
- `endpoint-model.yaml` configuration system
- `SchemaLoader` for resource management
- Base `EndpointModel` and `OperationModel` classes
- `StatsAPIObject` for HTTP requests and file operations
- Support for 20+ MLB Stats API endpoints

#### Core Features
- HTTP request handling with retry logic
- File system operations (save/load/gzip)
- Path and query parameter resolution
- Validation from JSON schemas
- Default storage in `./.var/local/mlb_statsapi`

---

## Migration & Compatibility

### Version Compatibility
- **Python**: 3.11, 3.12, 3.13 supported
- **Platforms**: Ubuntu, macOS, Windows tested in CI
- **Dependencies**: Minimal (requests)

### Breaking Changes
No breaking changes between development phases. All phases coexist:
- Original hardcoded models still available
- Dynamic system available as alternative
- Clean API refactor maintains backward compatibility
- Schema introspection adds methods without removing existing ones

### Migration Path
Users can adopt features gradually:
1. **Phase 1**: Start using dynamic system for new code
2. **Phase 2**: Add schema introspection for API discovery
3. **Phase 3**: Migrate to clean function signatures

Or continue using the original system - all approaches work.

---

## Future Roadmap

Planned enhancements for post-1.0 releases:

### API Improvements
- POST/PUT endpoint support (currently GET only)
- Async/await support for concurrent requests
- Batch request execution
- Automatic rate limit handling

### Developer Experience
- Generate type stubs from schemas (`.pyi` files)
- Create Pydantic models for validation
- Export to OpenAPI/Swagger format
- Interactive schema explorer CLI
- Generate mock data from schemas

### Documentation
- Auto-generate API docs from schemas
- Build documentation site from schemas
- Add more real-world usage examples
- Video tutorials and guides

### Testing
- Increase unit test coverage to >90%
- Add integration tests for all endpoints
- Performance benchmarking suite
- Capture comprehensive stub library

---

Future changes will be documented above following [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes
