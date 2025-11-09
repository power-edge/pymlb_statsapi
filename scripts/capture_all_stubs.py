#!/usr/bin/env python3
"""
Capture stubs for all available MLB StatsAPI endpoints.

This script systematically calls all available API methods with reasonable test data
and saves the responses as gzipped stubs for testing.

Usage:
    python scripts/capture_all_stubs.py [--endpoint ENDPOINT] [--delay SECONDS]

Options:
    --endpoint ENDPOINT  Only capture stubs for specified endpoint
    --delay SECONDS      Delay between API calls (default: 2)

Note:
    This script is designed to work with the BDD test infrastructure.
    Run with STUB_MODE=capture uv run behave to capture stubs instead.
"""

import argparse
import time

from pymlb_statsapi import api

# Test data for capturing stubs
# Using completed games and stable dates to ensure data doesn't change
TEST_DATA = {
    "schedule": [
        {"sportId": 1, "date": "2024-10-27"},  # World Series date
        {"sportId": 1, "date": "2024-10-27", "teamId": "147"},  # Yankees WS game
        {"sportId": 1, "startDate": "2024-10-01", "endDate": "2024-10-31"},
    ],
    "game": [
        {"game_pk": "747175"},  # World Series Game 1
        {"game_pk": "747176"},  # World Series Game 2
        {"game_pk": "747175", "timecode": "20241027_120000"},
    ],
    "team": [
        {"teamId": "147"},  # Yankees
        {"teamId": "119"},  # Dodgers
        {"sportId": 1, "season": "2024"},
    ],
    "person": [
        {"personId": "660271"},  # Aaron Judge
        {"personId": "665487"},  # Shohei Ohtani
    ],
    "season": [
        {"sportId": 1},
        {"seasonId": "2024"},
        {"seasonId": "2024", "sportId": 1},
    ],
    "stats": [
        {"group": "hitting", "stats": "season", "season": "2024", "sportId": 1},
        {"group": "pitching", "stats": "season", "season": "2024", "sportId": 1},
    ],
    "league": [
        {},  # Get all leagues
        {"leagueId": "103"},  # American League
    ],
    "division": [
        {"divisionId": "200"},  # AL East
    ],
    "sports": [
        {},  # Get all sports
        {"sportId": 1},  # Baseball
    ],
}


def capture_endpoint_stubs(endpoint_name: str, delay: float = 2.0):
    """
    Capture stubs for a specific endpoint.

    Args:
        endpoint_name: Name of the endpoint to capture
        delay: Delay between API calls in seconds
    """
    print(f"\n{'=' * 60}")
    print(f"Capturing stubs for endpoint: {endpoint_name}")
    print(f"{'=' * 60}\n")

    # Get the endpoint
    try:
        endpoint = api.get_endpoint(endpoint_name)
    except KeyError:
        print(f"❌ Endpoint '{endpoint_name}' not found")
        return

    # Get test data for this endpoint
    test_cases = TEST_DATA.get(endpoint_name, [{}])

    # Get all methods for this endpoint
    method_names = endpoint.get_method_names()
    print(f"Found {len(method_names)} methods: {', '.join(method_names)}\n")

    success_count = 0
    error_count = 0

    for method_name in method_names:
        # Skip internal methods
        if method_name.startswith("__"):
            continue

        print(f"  📋 Method: {method_name}")

        # Try each test case
        for i, params in enumerate(test_cases, 1):
            try:
                print(f"    Test case {i}/{len(test_cases)}: {params}")

                # Get the method
                method = getattr(endpoint, method_name)

                # Call with parameters
                response = method(**params)

                # Verify success
                if response.ok:
                    # Save as gzipped stub
                    result = response.gzip(prefix="captured-stubs")
                    print(f"    ✅ Success: {result['path']}")
                    success_count += 1
                else:
                    print(f"    ⚠️  Failed with status {response.status_code}")
                    error_count += 1

                # Rate limiting - be nice to the API
                time.sleep(delay)

            except Exception as e:
                print(f"    ❌ Error: {e}")
                error_count += 1

    print(f"\n✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Capture stubs for MLB StatsAPI endpoints")
    parser.add_argument(
        "--endpoint",
        help="Only capture stubs for specified endpoint",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between API calls in seconds (default: 2)",
    )
    args = parser.parse_args()

    # Get list of endpoints to capture
    if args.endpoint:
        endpoints = [args.endpoint]
    else:
        endpoints = sorted(api.get_endpoint_names())

    print("\n" + "=" * 60)
    print("MLB StatsAPI Stub Capture Script")
    print("=" * 60)
    print(f"Endpoints to capture: {len(endpoints)}")
    print(f"Delay between calls: {args.delay}s")
    print("Stubs will be saved as gzipped JSON files")
    print("=" * 60)

    # Capture stubs for each endpoint
    for endpoint_name in endpoints:
        try:
            capture_endpoint_stubs(endpoint_name, args.delay)
        except KeyboardInterrupt:
            print("\n\n⚠️  Capture interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            continue

    print("\n" + "=" * 60)
    print("Capture complete!")
    print("=" * 60)
    print("\nRun tests with: STUB_MODE=replay behave")


if __name__ == "__main__":
    main()
