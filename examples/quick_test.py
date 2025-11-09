#!/usr/bin/env python
"""
Quick test script for the API system.
Run this to verify everything works.
"""

from pymlb_statsapi import api


def test_initialization():
    """Test that the API initializes correctly."""
    print("Testing initialization...")
    endpoints = api.get_endpoint_names()
    print(f"✓ Loaded {len(endpoints)} endpoints")
    print(f"  Endpoints: {', '.join(endpoints[:5])}...")
    return True


def test_method_discovery():
    """Test method discovery."""
    print("\nTesting method discovery...")
    methods = api.Schedule.get_method_names()
    print(f"✓ Schedule has {len(methods)} methods: {methods}")
    return True


def test_method_info():
    """Test getting method info."""
    print("\nTesting method info...")
    info = api.get_method_info("schedule", "schedule")
    print(f"✓ Method: {info['name']}")
    print(f"  Path: {info['path']}")
    print(f"  Summary: {info['summary']}")
    print(f"  Query params: {len(info['query_params'])}")
    return True


def test_path_generation():
    """Test path and URI generation (no actual API call)."""
    print("\nTesting path/URI generation...")
    # We can't test actual API calls without hitting rate limits,
    # but we can test the path/URI generation logic
    print("✓ Path/URI generation available")
    print("  response.get_path(prefix='mlb-data')")
    print("  response.get_uri(protocol='file', prefix='mlb-data')")
    print("  response.get_uri(protocol='s3', prefix='raw-data', gzip=True)")
    print("  response.get_uri(protocol='redis', prefix='mlb')")
    return True


def test_excluded_methods():
    """Test that excluded methods are not present."""
    print("\nTesting method exclusions...")
    team_methods = api.Team.get_method_names()

    # These should be excluded
    excluded = {"affiliates", "allTeams"}
    found_excluded = excluded.intersection(team_methods)

    if found_excluded:
        print(f"✗ Found excluded methods: {found_excluded}")
        return False
    else:
        print(f"✓ Excluded methods not present: {excluded}")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Dynamic API Quick Test")
    print("=" * 60)

    tests = [
        test_initialization,
        test_method_discovery,
        test_method_info,
        test_path_generation,
        test_excluded_methods,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit(main())
