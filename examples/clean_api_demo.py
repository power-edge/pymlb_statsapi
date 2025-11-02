#!/usr/bin/env python3
"""
Demo of the new clean API with direct parameter passing.

Before (verbose):
    response = api.Game.liveGameV1(
        path_params={"game_pk": "747175"},
        query_params={"timecode": "20241027_000000"}
    )

After (clean):
    response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
"""

from pymlb_statsapi import api

# Example 1: Game endpoint with path and query params
print("=" * 60)
print("Example 1: Get live game data")
print("=" * 60)

# Clean API - just pass parameters directly!
response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print(f"Resource path: {response.get_path()}")

# Example 2: Schedule endpoint with query params only
print("\n" + "=" * 60)
print("Example 2: Get schedule")
print("=" * 60)

response = api.Schedule.schedule(sportId=1, date="2025-06-01")
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")
print(f"Resource path: {response.get_path(prefix='mlb-data')}")

# Example 3: Team endpoint
print("\n" + "=" * 60)
print("Example 3: Get team info")
print("=" * 60)

response = api.Team.team(teamId="147", season="2024")
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")

# Access response data
data = response.json()
if "teams" in data and len(data["teams"]) > 0:
    team = data["teams"][0]
    print(f"Team: {team.get('name', 'N/A')}")
    print(f"Venue: {team.get('venue', {}).get('name', 'N/A')}")

# Example 4: Save response
print("\n" + "=" * 60)
print("Example 4: Save response to file")
print("=" * 60)

result = response.save_json(prefix="demo")
print(f"Saved to: {result['path']}")
print(f"Bytes written: {result['bytes_written']}")

print("\n" + "=" * 60)
print("All parameters are now clean and Pythonic!")
print("No need to think about path_params vs query_params")
print("=" * 60)
