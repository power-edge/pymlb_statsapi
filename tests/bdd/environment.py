"""
Behave environment setup for MLB StatsAPI testing.

Stub mode is controlled by STUB_MODE environment variable:
- replay (default): Use existing stubs (fast, no API calls)
- capture: Make real API calls and save responses as stubs
- passthrough: Make real API calls without saving stubs
"""

import os

from tests.bdd.stub_manager import StubManager


def before_all(context):
    """Initialize test environment."""
    # Create stub manager
    context.stub_manager = StubManager()

    # Track captured stubs
    context.captured_stubs = []

    # Track test statistics
    context.stats = {
        "scenarios_run": 0,
        "scenarios_passed": 0,
        "scenarios_failed": 0,
        "stubs_captured": 0,
        "stubs_replayed": 0,
        "api_calls_made": 0,
    }

    # Default stub mode from environment or default to replay
    context.default_stub_mode = os.environ.get("STUB_MODE", "replay")

    print(f"\n{'=' * 60}")
    print("MLB StatsAPI Behave Tests")
    print(f"Default Stub Mode: {context.default_stub_mode}")
    print(f"Stub Directory: {context.stub_manager.stub_dir}")
    print(f"{'=' * 60}\n")


def after_all(context):
    """Cleanup and print statistics."""
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print(f"{'=' * 60}")
    print(f"Scenarios run: {context.stats['scenarios_run']}")
    print(f"Scenarios passed: {context.stats['scenarios_passed']}")
    print(f"Scenarios failed: {context.stats['scenarios_failed']}")
    print(f"API calls made: {context.stats['api_calls_made']}")
    print(f"Stubs captured: {context.stats['stubs_captured']}")
    print(f"Stubs replayed: {context.stats['stubs_replayed']}")

    if context.captured_stubs:
        print(f"\nCaptured {len(context.captured_stubs)} stubs:")
        for stub_path in context.captured_stubs:
            print(f"  - {stub_path}")

    print(f"{'=' * 60}\n")


def before_scenario(context, scenario):
    """Setup before each scenario."""
    context.stats["scenarios_run"] += 1

    # Use stub mode from environment variable
    context.stub_mode = context.default_stub_mode

    # Clear scenario-specific context
    context.response = None
    context.stub_data = None
    context.error = None


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if scenario.status == "passed":
        context.stats["scenarios_passed"] += 1
    else:
        context.stats["scenarios_failed"] += 1
