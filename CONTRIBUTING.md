# Contributing to PyMLB StatsAPI

Thank you for your interest in contributing to PyMLB StatsAPI! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Git

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pymlb_statsapi.git
   cd pymlb_statsapi
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/power-edge/pymlb_statsapi.git
   ```

4. **Install dependencies**:
   ```bash
   uv sync
   ```

5. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

## Development Workflow

### Creating a Feature Branch

Always create a new branch for your work:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications
- `chore/` - Maintenance tasks

### Making Changes

1. **Make your changes** following the [coding standards](#coding-standards)

2. **Run tests** to ensure nothing breaks:
   ```bash
   # Run unit tests
   uv run pytest

   # Run BDD tests (with stubs)
   STUB_MODE=replay uv run behave
   ```

3. **Run code quality checks**:
   ```bash
   # Linting
   uv run ruff check .

   # Formatting
   uv run ruff format .

   # Or run all pre-commit hooks
   uv run pre-commit run --all-files
   ```

4. **Commit your changes** using conventional commits:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Commit message format:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Formatting changes
   - `refactor:` - Code refactoring
   - `test:` - Test changes
   - `chore:` - Maintenance tasks

### Using the Git Helper Script

We provide a helper script for common git operations:

```bash
bash scripts/git.sh
```

This provides an interactive menu for:
1. Format & commit changes
2. Create release (bump version & tag)
3. Push to remote
4. Full release workflow
5. Status check

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests** and ensure they pass:
   ```bash
   uv run pytest --cov=pymlb_statsapi
   STUB_MODE=replay uv run behave
   ```

3. **Run code quality checks**:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run bandit -r pymlb_statsapi/ -ll
   ```

4. **Update documentation** if needed

### Submitting the Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub

3. **Fill out the PR template** completely:
   - Describe your changes
   - Link related issues
   - List any breaking changes
   - Include screenshots if applicable

4. **Wait for CI checks** to complete:
   - All tests must pass
   - Code coverage should not decrease significantly
   - Linting and formatting checks must pass

5. **Address review feedback** promptly:
   - Make requested changes
   - Push updates to your branch
   - Respond to comments

### PR Review Process

- PRs require at least **1 approving review** from a maintainer
- All CI checks must pass (tests, linting, build, docs)
- Conversations must be resolved before merging
- Maintainers may request changes or ask questions

## Coding Standards

### Python Style Guide

- **Line length**: 100 characters maximum
- **Python version**: 3.11+ features allowed
- **Style**: Follow PEP 8 (enforced by ruff)
- **Type hints**: Use type annotations where appropriate
- **Docstrings**: Use Google-style docstrings

### Key Principles

1. **Schema is Truth**: JSON schemas define everything
2. **No Hardcoding**: Generate, don't write
3. **Parameter Naming**: Preserve exact names from schemas (no camelCase conversion)
4. **Testing**: All new features need tests
5. **Documentation**: Update docs for user-facing changes

### Code Example

```python
from pymlb_statsapi import api

# Good: Clean, schema-driven parameter passing
response = api.Schedule.schedule(sportId=1, date="2024-10-27")
data = response.json()

# Bad: Don't create hardcoded classes or models
class Schedule:  # Don't do this!
    def __init__(self, sport_id: int):
        self.sport_id = sport_id
```

## Testing

### Unit Tests

- Located in `tests/unit/`
- Use pytest
- Aim for high coverage of new code

```bash
# Run unit tests
uv run pytest

# With coverage
uv run pytest --cov=pymlb_statsapi --cov-report=html

# Specific test
uv run pytest tests/unit/pymlb_statsapi/model/test_factory.py
```

### BDD Tests

- Located in `tests/bdd/`
- Use behave with stub capture/replay
- Test real-world API scenarios

```bash
# Run with stubs (fast)
STUB_MODE=replay uv run behave

# Capture new stubs (makes real API calls)
STUB_MODE=capture uv run behave features/schedule.feature

# Test specific endpoint
uv run behave features/game.feature
```

### Test Data Guidelines

- Use **completed games** from past seasons
- Example: World Series 2024 games (game_pk=747175, 747176)
- Use stable dates: October 2024 for schedules
- Always gzip test stubs

## Documentation

### Updating Documentation

Documentation is built with Sphinx and hosted on ReadTheDocs.

```bash
# Build documentation locally
cd docs
make html

# View in browser
open _build/html/index.html
```

### Documentation Guidelines

- Update docstrings for new methods
- Add examples for new features
- Update schema reference if schemas change
- Keep README.md examples up to date

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check documentation** for solutions
3. **Test with latest version**

### Creating a Good Issue

- Use issue templates (bug report or feature request)
- Provide clear, concise description
- Include code examples and error messages
- Specify Python version and OS
- Include relevant logs or screenshots

### Issue Labels

Maintainers will label issues:
- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested

## Adding New Endpoints

When MLB adds new endpoints:

1. **Get JSON schema** from MLB Stats API documentation
2. **Add to resources**: `pymlb_statsapi/resources/schemas/statsapi/stats_api_1_0/{endpoint}.json`
3. **Create BDD tests**: `tests/bdd/{endpoint}.feature`
4. **Capture stubs**: `STUB_MODE=capture uv run behave tests/bdd/{endpoint}.feature`
5. **Update documentation**: Add examples to schema reference

No code changes needed - the system is fully schema-driven!

## Getting Help

- **GitHub Discussions**: Ask questions and discuss ideas
- **Issue Tracker**: Report bugs or request features
- **Documentation**: Read the full docs at https://pymlb-statsapi.readthedocs.io/

## Recognition

Contributors will be:
- Listed in release notes
- Acknowledged in the project
- Added to GitHub contributors page

Thank you for contributing to PyMLB StatsAPI!
