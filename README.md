# PyMLB StatsAPI

[![PyPI version](https://badge.fury.io/py/pymlb-statsapi.svg)](https://badge.fury.io/py/pymlb-statsapi)
[![Documentation Status](https://readthedocs.org/projects/pymlb-statsapi/badge/?version=latest)](https://pymlb-statsapi.readthedocs.io/en/latest/)
[![Tests](https://github.com/power-edge/pymlb_statsapi/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/power-edge/pymlb_statsapi/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/power-edge/pymlb_statsapi/branch/main/graph/badge.svg)](https://codecov.io/gh/power-edge/pymlb_statsapi)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/power-edge/pymlb_statsapi?style=social)](https://github.com/power-edge/pymlb_statsapi/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/power-edge/pymlb_statsapi?style=social)](https://github.com/power-edge/pymlb_statsapi/network/members)

A clean, Pythonic wrapper for MLB Stats API endpoints with automatic schema-driven parameter validation.

## ✨ Features

- **🎯 Clean API**: Parameters are intelligently routed to path or query params based on the schema configuration
- **🪶 Lean**: Only requires `requests` - no heavy dependencies
- **📋 Schema-driven**: All endpoints and methods generated from JSON schemas (sourced from https://beta-statsapi.mlb.com/docs/ - now offline)
- **✅ Type-safe**: Automatic parameter validation from API schemas
- **🔄 Dynamic**: Zero hardcoded models - updates via schema changes only
- **🧪 Well-tested**: Comprehensive unit tests with pytest and BDD test suite with stub capture/replay
- **📚 Self-documenting**: Auto-generated docstrings from API schemas
- **🚀 Fast**: Stub-based testing runs in <1 second

## 🚀 Quick Start

### Installation

```bash
# With pip
pip install pymlb-statsapi

# With uv (recommended)
uv add pymlb-statsapi
```

### Basic Usage

```python
from pymlb_statsapi import api

# Get schedule (clean parameter passing!)
response = api.Schedule.schedule(sportId=1, date="2025-06-01")
data = response.json()

# Get live game data
response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
data = response.json()

# Get team information
response = api.Team.team(teamId="147", season="2024")
team_data = response.json()

# Save response to file
result = response.save_json(prefix="mlb-data")
print(f"Saved to: {result['path']}")
```

## 📖 Documentation

### 🔍 Start Here: Schema Reference

The **[Schema Reference](https://pymlb-statsapi.readthedocs.io/en/latest/schemas/index.html)** is the heart of this library - browse all 21 MLB Stats API endpoints with detailed parameter docs and working examples for every method.

### Additional Resources

- **[Full Documentation](https://pymlb-statsapi.readthedocs.io/)** - Complete guide on ReadTheDocs
- **[API Reference](https://pymlb-statsapi.readthedocs.io/en/latest/api/factory.html)** - Implementation documentation
- **Examples** - Check the `examples/` directory for working code samples
- **Testing Guide** - See the [Testing](https://pymlb-statsapi.readthedocs.io/en/latest/testing.html) documentation

## 🏗️ Architecture

### Config-Driven Design

All MLB API endpoints are defined as JSON schemas rather than hardcoded. These schemas were sourced from the MLB Stats API Beta documentation site (https://beta-statsapi.mlb.com/docs/), which is no longer publicly available:

```
pymlb_statsapi/resources/schemas/statsapi/stats_api_1_0/
├── schedule.json  → Schedule endpoint with methods
├── game.json      → Game endpoint (live feed, boxscore, etc.)
├── team.json      → Team endpoint (roster, stats, etc.)
├── person.json    → Person endpoint (player data)
└── ...
```

Each schema defines which parameters are path parameters vs query parameters. Method paths are mapped in `endpoint-model.json`:

```json
{
  "schedule": {
    "schedule": {
      "path": "/v1/schedule",
      "name": "schedule"
    },
    "tieGames": {
      "path": "/v1/schedule/games/tied",
      "name": "tieGames"
    }
  }
}
```

### Clean API: Intelligent Parameter Routing

The "Clean API" intelligently routes parameters to the underlying path or query parameters based on each method's schema configuration:

```python
# The library automatically determines parameter types from the schema
response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
# Resolves to: /api/v1/game/747175/feed/live?timecode=20241027_000000

response = api.Schedule.schedule(sportId=1, date="2025-06-01")
# Resolves to: /api/v1/schedule?sportId=1&date=2025-06-01
```

### Key Components

**Dynamic Factory (`factory.py`):**
- Generates endpoint classes and methods from schemas at runtime
- Creates clean function signatures with proper parameter handling
- Handles method overloading (e.g., `seasons()` with/without `seasonId`)

**Registry (`registry.py`):**
- Central `api` singleton that loads all endpoints
- Provides discovery API for exploring available methods

**API Response (`factory.py: APIResponse`):**
- Wraps `requests.Response` with metadata
- Provides `.json()`, `.save_json()`, `.get_path()`, `.get_uri()` methods
- Generates consistent resource paths for file storage

## 🎓 Examples

### Working with Different Endpoints

```python
from pymlb_statsapi import api

# Schedule queries
response = api.Schedule.schedule(
    sportId=1,
    date="2024-10-27",
    teamId="147"
)

# Get all teams
response = api.Team.teams(sportId=1, season="2024")

# Get player information
response = api.Person.people(personId="660271")

# Get season information (overloaded method)
response = api.Season.seasons(sportId=1)  # All seasons
response = api.Season.seasons(seasonId="2024")  # Specific season

# Get game stats
response = api.Stats.stats(
    group="hitting",
    stats="season",
    season="2024",
    sportId=1
)
```

### File Storage

```python
# Auto-generate file path
result = response.save_json(prefix="mlb-data")
print(f"Saved to: {result['path']}")
print(f"Bytes written: {result['bytes_written']}")

# Explicit file path
response.save_json("/path/to/file.json")

# Gzipped JSON
response.save_json(gzip=True, prefix="mlb-data")
```

### URI Generation for Different Protocols

```python
# File protocol (default)
uri = response.get_uri(protocol="file", prefix="mlb-data")
# Result: file:///path/to/.var/local/mlb_statsapi/mlb-data/schedule/schedule/date=2025-06-01.json

# S3 protocol (requires PYMLB_STATSAPI__S3_BUCKET env var)
uri = response.get_uri(protocol="s3", prefix="raw-data", gzip=True)
# Result: s3://my-bucket/raw-data/schedule/schedule/date=2025-06-01.json.gz

# Redis protocol
uri = response.get_uri(protocol="redis", prefix="mlb")
# Result: redis://localhost:6379/0/mlb/schedule/schedule/date=2025-06-01
```

### API Discovery

```python
# List all available endpoints
print(api.get_endpoint_names())
# ['schedule', 'game', 'team', 'person', 'season', ...]

# List methods for an endpoint
endpoint = api.get_endpoint("schedule")
print(endpoint.get_method_names())
# ['schedule', 'tieGames', 'postseason', ...]

# Get detailed method information
info = api.get_method_info("schedule", "schedule")
print(info["path"])          # /v1/schedule
print(info["summary"])       # View schedule info
print(info["path_params"])   # []
print(info["query_params"])  # [{"name": "sportId", ...}, ...]
```

## 🧪 Testing

### Unit Tests

```bash
# Run unit tests
pytest

# With coverage
pytest --cov=pymlb_statsapi --cov-report=html

# Specific test file
pytest tests/unit/pymlb_statsapi/model/test_factory.py
```

### BDD Tests with Stubs (Fast)

```bash
# Run all BDD tests with stubs (completes in <1 second)
behave

# Or explicitly
STUB_MODE=replay behave
```

### Capture Fresh Stubs

```bash
# Capture stubs by making real API calls
STUB_MODE=capture behave

# Capture stubs for specific endpoint
STUB_MODE=capture behave features/schedule.feature
```

### Run Specific BDD Tests

```bash
# Test specific feature
behave features/game.feature

# Verbose output
behave -v features/season.feature

# Test with specific tag
behave --tags=@game
```

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/power-edge/pymlb_statsapi.git
cd pymlb_statsapi

# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install
```

### Code Quality

```bash
# Linting
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Formatting
ruff format .

# Run all pre-commit hooks
pre-commit run --all-files

# Security scan
bandit -r pymlb_statsapi/
```

### Building

```bash
# Build package
hatch build

# Or with uv
uv build

# Version is auto-generated from git tags via hatch-vcs
```

### Publishing

For local publishing (requires .env configuration):

```bash
# Set up credentials
cp .env.example .env
# Edit .env with your PyPI tokens

# Publish to TestPyPI (for testing)
./scripts/publish.sh testpypi

# Publish to PyPI (production)
./scripts/publish.sh pypi
```

For automated publishing, use GitHub Actions:
- Push a version tag (e.g., `v1.2.0`) to trigger automatic PyPI publishing
- Configure `PYPI_TOKEN` secret in GitHub repository settings

## 📊 Test Coverage

- **30 unit tests** with pytest covering core functionality
- **39 BDD scenarios** covering all major endpoints
- **277 test steps** with path/query parameter variations
- **Stub-based testing** for fast, deterministic CI/CD
- **Real-world data** using completed games (October 2024 World Series)

## 🌟 Support This Project

If you find this library useful, consider supporting its development:

- **[☕ Buy Me A Coffee](https://www.buymeacoffee.com/nikolauspschuetz)**
- **[💖 Ko-fi](https://ko-fi.com/nikolauspschuetz)**

[//]: # (- **[🎯 Patreon]&#40;https://www.patreon.com/YOUR_PATREON_USERNAME&#41;**)
[//]: # (- **[💰 GitHub Sponsors]&#40;https://github.com/sponsors/YOUR_GITHUB_USERNAME&#41;**)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to fork the repository and submit a Pull Request.

We have a git helper for common operations, see `scripts/git.sh`
```shell
================================
   Git Workflow Helper
================================
1) Format & commit changes
2) Create release (bump version & tag)
3) Push to remote
4) Full release (format, commit, bump, tag, push, build)
5) Status
6) Exit
```

## 🔗 Links

- **[Documentation](https://pymlb-statsapi.readthedocs.io/)**
- **[PyPI Package](https://pypi.org/project/pymlb-statsapi/)**
- **[GitHub Repository](https://github.com/power-edge/pymlb_statsapi)**
- **[Issue Tracker](https://github.com/power-edge/pymlb_statsapi/issues)**
- **[MLB Stats API Docs](https://statsapi.mlb.com/docs/)**

## 🙏 Acknowledgments

- Built on the excellent [MLB Stats API](https://statsapi.mlb.com/)
- Inspired by various MLB data projects in the community
- Thanks to all contributors!

---

**Made with ❤️ by the PyMLB StatsAPI Team**
