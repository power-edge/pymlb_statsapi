"""
Entity Relationships Example
Shows how to traverse related data using the API structure
"""

from pymlb_statsapi import api


def demonstrate_data_flow():
    """Show the core data flow: Season → Schedule → Game → Teams/Players → Stats"""

    print("=== MLB Data Entity Relationships Demo ===\n")

    # 1. Season (temporal context)
    print("1. Getting season information...")
    season_response = api.Season.seasons(seasonId=2024)
    season_data = season_response.json()
    print(
        f"Season: {season_data['seasons'][0]['seasonId']} - {season_data['seasons'][0]['seasonDisplayName']}"
    )

    # 2. Schedule (games for a date)
    print("\n2. Getting schedule for World Series...")
    schedule_response = api.Schedule.schedule(sportId=1, date="2024-10-27")
    schedule_data = schedule_response.json()

    if schedule_data["dates"]:
        games = schedule_data["dates"][0]["games"]
        game = games[0]  # First game of the day
        game_pk = game["gamePk"]
        print(
            f"Game: {game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']}"
        )
        print(f"Game PK: {game_pk}")

        # 3. Game (live data with relationships)
        print("\n3. Getting live game data...")
        game_response = api.Game.liveGameV1(game_pk=game_pk)
        game_data = game_response.json()

        # Show nested relationships
        home_team_id = game_data["gameData"]["teams"]["home"]["id"]
        away_team_id = game_data["gameData"]["teams"]["away"]["id"]
        print(f"Home Team ID: {home_team_id}")
        print(f"Away Team ID: {away_team_id}")

        # 4. Team (roster and stats)
        print("\n4. Getting team roster...")
        roster_response = api.Team.roster(teamId=home_team_id, rosterType="active")
        roster_data = roster_response.json()

        if roster_data["roster"]:
            player = roster_data["roster"][0]["person"]
            player_id = player["id"]
            print(f"Sample Player: {player['fullName']} (ID: {player_id})")

            # 5. Person (player stats)
            print("\n5. Getting player information...")
            person_response = api.Person.person(personId=player_id)
            person_data = person_response.json()

            if person_data["people"]:
                player_info = person_data["people"][0]
                print(f"Position: {player_info.get('primaryPosition', {}).get('name', 'N/A')}")
                print(f"Current Team: {player_info.get('currentTeam', {}).get('name', 'N/A')}")

        # 6. Stats (performance data)
        print("\n6. Getting team stats...")
        stats_response = api.Stats.stats(
            group="hitting", stats="season", season=2024, teamId=home_team_id
        )
        stats_data = stats_response.json()
        print(f"Stats available: {len(stats_data.get('stats', []))} stat groups")


def demonstrate_timecode_usage():
    """Show how timecode creates historical snapshots"""

    print("\n=== Timecode Historical Snapshots ===\n")

    game_pk = 747175  # World Series Game 1

    # Latest data (no timecode)
    print("Latest game state:")
    latest_response = api.Game.liveGameV1(game_pk=game_pk)
    latest_data = latest_response.json()
    print(
        f"Current inning: {latest_data.get('liveData', {}).get('linescore', {}).get('currentInning', 'N/A')}"
    )

    # Historical snapshot (with timecode)
    print("\nHistorical snapshot (game start):")
    historical_response = api.Game.liveGameV1(game_pk=game_pk, timecode="20241027_000000")
    historical_data = historical_response.json()
    print(
        f"Inning at start: {historical_data.get('liveData', {}).get('linescore', {}).get('currentInning', 'N/A')}"
    )

    print("\nThis demonstrates how the same endpoint produces different materialized tables:")
    print("- game_live_data (latest snapshot)")
    print("- game_live_data_timecode (historical snapshots)")


def demonstrate_reference_vs_event_data():
    """Show different data patterns for ETL"""

    print("\n=== Data Patterns for ETL ===\n")

    # Reference data (slowly changing)
    print("Reference Data (teams - rarely change):")
    teams_response = api.Team.teams(sportId=1, season=2024)
    teams_data = teams_response.json()
    print(f"Total teams: {len(teams_data.get('teams', []))}")

    # Event data (append-only)
    print("\nEvent Data (schedule - historical record):")
    schedule_response = api.Schedule.schedule(sportId=1, date="2024-10-27")
    schedule_data = schedule_response.json()
    print(f"Games on date: {schedule_data.get('totalGames', 0)}")

    # Time-series data (multiple snapshots)
    print("\nTime-series Data (stats - change over time):")
    stats_response = api.Stats.leaders(leaderCategories="homeRuns", season=2024, sportId=1)
    stats_data = stats_response.json()
    print(f"Home run leaders: {len(stats_data.get('leagueLeaders', [{}])[0].get('leaders', []))}")


if __name__ == "__main__":
    demonstrate_data_flow()
    demonstrate_timecode_usage()
    demonstrate_reference_vs_event_data()

    print("\n=== Summary ===")
    print("This example shows how entities relate to each other:")
    print("Season → Schedule → Game → Teams/Players → Stats")
    print("\nFor ETL purposes, consider:")
    print("- Reference data: Teams, players, config (infrequent updates)")
    print("- Event data: Schedules, games, awards (append-only)")
    print("- Time-series: Live game data, stats (frequent snapshots)")
