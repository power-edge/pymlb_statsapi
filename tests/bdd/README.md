---
# MLB StatsAPI Behave Tests

End-to-end testing for the PyMLB StatsAPI dynamic model with stub capture and replay.

## Overview

This test suite provides:
- **Comprehensive endpoint coverage**: Tests for all major MLB StatsAPI endpoints
- **Stub capture/replay**: Save real API responses as stubs for fast, deterministic testing
- **Real-world data**: Uses completed games from October 2024 (World Series) so responses don't change
- **Method overloading tests**: Validates the dynamic API's overloaded methods work correctly

## Quick Start

### 1. Capture Stubs (First Time)

Make real API calls and save responses as stubs:

```bash
STUB_MODE=capture behave
```

This will:
- Make real API calls to MLB StatsAPI
- Save all responses as JSON files in `features/stubs/`
- Organize stubs by endpoint, method, and parameters

### 2. Run Tests with Stubs (Fast)

Use saved stubs for fast testing:

```bash
behave
```

Or explicitly:

```bash
STUB_MODE=replay behave
```

This will:
- Use saved stubs instead of making API calls
- Run tests in ~1 second (vs minutes for real API calls)
- Work offline

### 3. Run Tests by Tag

All feature files are tagged with `@schema:<SchemaName>` and scenarios are tagged with `@method:<methodName>`.

Run tests by schema:
```bash
# Test all Schedule endpoints
behave --tags=@schema:Schedule

# Test all Game endpoints
behave --tags=@schema:Game

# Test all Person endpoints
behave --tags=@schema:Person
```

Run tests by method:
```bash
# Test only the boxscore method
behave --tags=@method:boxscore

# Test only schedule-related methods
behave --tags=@method:schedule

# Test multiple methods
behave --tags=@method:liveGameV1,@method:playByPlay
```

Combine schema and method tags:
```bash
# Test only Game.boxscore
behave --tags=@schema:Game --tags=@method:boxscore

# Test Schedule schema, but exclude tieGames method
behave --tags=@schema:Schedule --tags=~@method:tieGames
```

### 4. Run Specific Features

```bash
# Test only schedule endpoint
behave features/schedule.feature

# Test only game endpoint
behave features/game.feature

# Test with verbose output
behave -v features/season.feature
```

## Stub Modes

Control stub behavior via the `STUB_MODE` environment variable or by using tags:

### Environment Variable (Global)

Set `STUB_MODE` to control all tests:

| Mode | Behavior |
|------|----------|
| `replay` (default) | Use existing stubs. Fail if stub not found. Fast, no API calls. |
| `capture` | Make real API calls and save as stubs. Overwrites existing stubs. |
| `passthrough` | Make real API calls without saving stubs. For debugging. |

```bash
# Capture all stubs
STUB_MODE=capture uv run behave

# Replay from stubs (default)
STUB_MODE=replay uv run behave
# or just:
uv run behave

# Make real calls without saving
STUB_MODE=passthrough uv run behave
```

### Tags (Fine-Grained Control)

You can also control stub mode per feature or scenario using tags. Tags are processed using behave's `before_tag` hook, which provides clean, global control:

```gherkin
@capture
Feature: My Feature
  # All scenarios in this feature will capture stubs

@replay
Scenario: My scenario
  # This specific scenario will replay from stubs
```

**How it works:**
- Tags are processed via the `before_tag` hook in `environment.py`
- When a stub mode tag (`@capture`, `@replay`, `@passthrough`) is encountered, it sets the mode globally for that context
- Scenario-level tags are processed after feature-level tags, naturally giving them higher precedence
- After each scenario, the stub mode resets to the default

Tag precedence: Scenario tags > Feature tags > STUB_MODE env var

**Available tags:**
- `@capture` - Make real API calls and save responses
- `@replay` - Use existing stubs (fail if not found)
- `@passthrough` - Make real API calls without saving

## Directory Structure

```
features/
├── README.md              # This file
├── environment.py         # Behave setup (stub manager initialization)
├── stub_manager.py        # Stub capture/replay logic
├── steps/
│   └── statsapi_steps.py  # Step definitions for dynamic API
├── stubs/                 # Captured API responses (gitignored)
│   ├── schedule/
│   │   └── schedule/
│   │       └── schedule_date=2024-10-27_sportId=1_abc123.json
│   ├── game/
│   │   ├── boxscore/
│   │   ├── liveGameV1/
│   │   └── playByPlay/
│   └── ...
└── *.feature             # Feature files (test scenarios)
```

## Feature Files

### Core Endpoints

- **schedule.feature**: Schedule queries for specific dates, teams, postseason
- **game.feature**: Game data (boxscore, play-by-play, live feed)
- **team.feature**: Team info, rosters, coaches, stats
- **person.feature**: Player info, awards, free agents
- **season.feature**: Season info (demonstrates method overloading)
- **stats.feature**: Player stats (season, career, by group)
- **league_division_sport.feature**: Reference data

### Test Coverage

Each feature includes:
- **Scenario Outlines**: Data-driven tests with multiple examples
- **Path/Query Parameter Variations**: Tests different parameter combinations
- **Completed Game Data**: Uses World Series 2024 games (game_pk 747175, etc.)
- **Stable Dates**: October 2024 dates ensure data doesn't change

## Writing New Tests

### Basic Test Structure

```gherkin
Feature: My New Endpoint
  Test description

  Background:
    Given I use the myendpoint endpoint

  Scenario: Test something
    Given I call the mymethod method
    And I use path parameters: {"param": "value"}
    And I use query parameters: {"query": "value"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field someField
```

### Available Step Definitions

**Setup:**
- `Given I use the {endpoint_name} endpoint`
- `Given I call the {method_name} method`
- `Given I use path parameters: {json}`
- `Given I use query parameters: {json}`
- `Given I use no path parameters`
- `Given I use no query parameters`

**Execution:**
- `When I make the API call`

**Assertions:**
- `Then the response should be successful`
- `Then the response should contain the field {field}`
- `Then the response should contain a list in {field}`
- `Then the response should not be empty`
- `Then the resource path should match the pattern {pattern}`
- `Then the {list_field} should have at least {count:d} items`
- `Then each item in {list_field} should have {required_field}`
- `Then I can save the response to a file`

## Stub File Format

Stubs are JSON files with this structure:

```json
{
  "endpoint": "schedule",
  "method": "schedule",
  "path_params": {},
  "query_params": {"sportId": "1", "date": "2024-10-27"},
  "url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-10-27",
  "status_code": 200,
  "response": {
    "dates": [...]
  }
}
```

## Best Practices

### 1. Use Completed Games

Always use games that are finished (dates in the past) so data remains stable:

```gherkin
# Good - October 2024 World Series (complete)
Examples:
  | game_pk |
  | 747175  |
  | 747176  |

# Bad - Today's games (data changes)
Examples:
  | date       |
  | 2025-10-29 |
```

### 2. Test Method Overloading

For endpoints with overloaded methods, test both variants:

```gherkin
Scenario: Base variant (no path params)
  Given I call the seasons method
  And I use no path parameters
  And I use query parameters: {"sportId": 1}
  When I make the API call
  Then the response should be successful

Scenario: Parameterized variant (with path params)
  Given I call the seasons method
  And I use path parameters: {"seasonId": "2024"}
  And I use no query parameters
  When I make the API call
  Then the response should be successful
```

### 3. Use Scenario Outlines for Data Variations

```gherkin
Scenario Outline: Test multiple teams
  Given I call the teams method
  And I use query parameters: {"teamId": <team_id>}
  When I make the API call
  Then the response should be successful

  Examples:
    | team_id |
    | 147     |
    | 121     |
    | 111     |
```

## Continuous Integration

### GitHub Actions Example

```yaml
- name: Run behave tests (with stubs)
  run: |
    STUB_MODE=replay behave
```

### Capturing Fresh Stubs

Periodically refresh stubs (e.g., start of each season):

```bash
# Capture stubs for 2025 season
STUB_MODE=capture behave

# Commit updated stubs
git add features/stubs/
git commit -m "Update stubs for 2025 season"
```

## Troubleshooting

### "Stub not found" Error

```
AssertionError: Stub not found for schedule.schedule (path={}, query={'sportId': '1', 'date': '2024-10-27'})
```

**Solution**: Capture the stub first:
```bash
STUB_MODE=capture behave features/schedule.feature
```

### Stub Hash Mismatch

If parameters change slightly (order, types), the hash changes and stub won't be found.

**Solution**: Delete old stubs and recapture:
```bash
rm -rf features/stubs/schedule/schedule/
STUB_MODE=capture behave features/schedule.feature
```

### API Rate Limiting

When capturing many stubs:

```bash
# Capture one feature at a time
STUB_MODE=capture behave features/schedule.feature
sleep 5
STUB_MODE=capture behave features/game.feature
```

## See Also

- [Main README](../README.md)
- [Schema Introspection Guide](../SCHEMA_INTROSPECTION.md)
- [Behave Documentation](https://behave.readthedocs.io/)
