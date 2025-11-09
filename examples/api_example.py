"""
Example usage of the dynamic API system.

This demonstrates the new config-driven approach that eliminates hardcoded models.
"""

from pymlb_statsapi import api


def example_schedule():
    """Fetch schedule data."""
    print("\n=== Schedule Example ===")

    # Fetch schedule for a specific date
    response = api.Schedule.schedule(sportId=1, date="2024-07-04")

    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    print(f"Path: {response.get_path(prefix='mlb-data')}")

    # Get the data
    data = response.json()
    if "dates" in data and data["dates"]:
        games_count = sum(len(d.get("games", [])) for d in data["dates"])
        print(f"Games found: {games_count}")


def example_game_live():
    """Fetch live game data."""
    print("\n=== Live Game Example ===")

    # Note: Use a real game_pk for actual testing
    try:
        response = api.Game.liveGameV1(game_pk=746801)  # Example game

        print(f"Status: {response.status_code}")
        print(f"URL: {response.url}")

        data = response.json()
        game_data = data.get("gameData", {})
        game = game_data.get("game", {})
        print(f"Game: {game.get('type', 'N/A')} - {game.get('season', 'N/A')}")

    except AssertionError as e:
        print(f"Request failed: {e}")


def example_team_roster():
    """Fetch team roster."""
    print("\n=== Team Roster Example ===")

    # Yankees roster (teamId=147)
    response = api.Team.roster(teamId=147, rosterType="active")

    print(f"Status: {response.status_code}")
    print(f"Path: {response.get_path(prefix='mlb-data')}")

    data = response.json()
    roster = data.get("roster", [])
    print(f"Roster size: {len(roster)}")

    # Show first few players
    for player in roster[:3]:
        person = player.get("person", {})
        position = player.get("position", {})
        print(f"  - {person.get('fullName')}: {position.get('name')}")


def example_path_and_uri_generation():
    """Demonstrate path and URI generation for different storage backends."""
    print("\n=== Path & URI Generation Example ===")

    # Same request, different parameter order
    r1 = api.Team.teams(sportId=1, season="2024")
    r2 = api.Team.teams(season="2024", sportId=1)

    # Paths are consistent regardless of parameter order
    path1 = r1.get_path(prefix="mlb-data")
    path2 = r2.get_path(prefix="mlb-data")
    print(f"Path 1: {path1}")
    print(f"Path 2: {path2}")
    print(f"Paths match: {path1 == path2}")  # Should be True

    # Generate URIs as ParseResult objects
    print("\n=== ParseResult URI Examples ===")

    # File URI
    file_uri = r1.get_uri(protocol="file", prefix="mlb-data")
    print("\nFile URI:")
    print(f"  scheme: {file_uri.scheme}")
    print(f"  path: {file_uri.path}")
    print(f"  full: {file_uri.geturl()}")

    # File URI with gzip
    file_gz_uri = r1.get_uri(protocol="file", prefix="mlb-data", gzip=True)
    print("\nFile URI (gzipped):")
    print(f"  path: {file_gz_uri.path}")
    print(f"  full: {file_gz_uri.geturl()}")

    # Redis URI
    redis_uri = r1.get_uri(protocol="redis", prefix="mlb")
    print("\nRedis URI:")
    print(f"  scheme: {redis_uri.scheme}")
    print(f"  netloc (host:port): {redis_uri.netloc}")
    print(f"  path (db/key): {redis_uri.path}")
    print(f"  full: {redis_uri.geturl()}")

    # Example: Use with Redis (commented out)
    # import redis
    # from urllib.parse import urlparse
    # client = redis.Redis(host=redis_uri.netloc.split(':')[0],
    #                      port=int(redis_uri.netloc.split(':')[1]))
    # db_key = redis_uri.path  # e.g. '/0/mlb/team/teams/...'
    # client.setex(db_key, 3600, r1.text)  # Cache for 1 hour

    # S3 example (requires PYMLB_STATSAPI__S3_BUCKET env var)
    # import os
    # os.environ['PYMLB_STATSAPI__S3_BUCKET'] = 'my-bucket'
    # s3_uri = r1.get_uri(protocol='s3', prefix='raw-data', gzip=True)
    # print(f"\nS3 URI:")
    # print(f"  scheme: {s3_uri.scheme}")
    # print(f"  netloc (bucket): {s3_uri.netloc}")
    # print(f"  path: {s3_uri.path}")
    # print(f"  full: {s3_uri.geturl()}")  # s3://bucket/path


def example_save_response():
    """Save response to file with different formats."""
    print("\n=== Save Response Example ===")

    import os
    import tempfile

    response = api.Schedule.schedule(sportId=1, date="2024-07-04")

    # Example 1: Save to explicit path
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "mlb_schedule.json")
    result = response.save_json(file_path)
    print(f"Explicit path saved to: {result['path']}")
    print(f"Bytes written: {result['bytes_written']}")
    if os.path.exists(file_path):
        os.remove(file_path)

    # Example 2: Auto-generate path with prefix (returns URI ParseResult)
    result = response.save_json(prefix="test-data")
    print("\nAuto-generated with URI:")
    print(f"  path: {result['path']}")
    print(f"  bytes: {result['bytes_written']}")
    print(f"  uri.scheme: {result['uri'].scheme}")
    print(f"  uri.geturl(): {result['uri'].geturl()}")
    if os.path.exists(result["path"]):
        os.remove(result["path"])

    # Example 3: Save as gzipped (convenience method)
    result = response.gzip(prefix="test-data")
    print("\nGzipped file:")
    print(f"  path: {result['path']}")
    print(f"  uri: {result['uri'].geturl()}")
    if os.path.exists(result["path"]):
        os.remove(result["path"])

    print("\nCleaned up temp files")


def example_discovery():
    """Discover available endpoints and methods."""
    print("\n=== API Discovery Example ===")

    # List all endpoints
    endpoints = api.get_endpoint_names()
    print(f"Available endpoints ({len(endpoints)}): {', '.join(endpoints[:5])}...")

    # List methods for an endpoint
    schedule_methods = api.Schedule.get_method_names()
    print(f"\nSchedule methods: {schedule_methods}")

    # Get detailed info about a method
    info = api.get_method_info("schedule", "schedule")
    print(f"\nMethod: {info['name']}")
    print(f"Path: {info['path']}")
    print(f"Summary: {info['summary']}")
    print(f"Query parameters: {len(info['query_params'])}")


def example_error_handling():
    """Demonstrate error handling."""
    print("\n=== Error Handling Example ===")

    try:
        # Invalid game_pk
        response = api.Game.boxscore(game_pk=999999999)
        data = response.json()
        return data
    except AssertionError as e:
        print(f"Caught validation/HTTP error: {str(e)[:100]}...")

    try:
        # Missing required parameter
        response = api.Game.boxscore()
    except AssertionError as e:
        print(f"Caught missing parameter error: {str(e)[:100]}...")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Dynamic API Examples")
    print("=" * 60)

    # Run examples (comment out any that hit rate limits)
    example_discovery()
    example_schedule()
    # example_game_live()  # Uncomment with valid game_pk
    # example_team_roster()  # Uncomment to test
    example_path_and_uri_generation()
    # example_save_response()  # Uncomment to test file saving
    example_error_handling()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
