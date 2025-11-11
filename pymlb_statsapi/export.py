"""
Schema Export Utilities
Export API structure for ETL and data pipeline generation
"""

import json
from pathlib import Path


def export_endpoint_schema():
    """Export complete endpoint and method structure"""
    from . import api

    schema = {
        "api_version": "1.0",
        "exported_at": "2024-11-11T00:00:00Z",
        "endpoints": {},
        "method_count": 0,
    }

    total_methods = 0

    for endpoint_name in api.get_endpoint_names():
        endpoint = api.get_endpoint(endpoint_name)
        method_names = endpoint.get_method_names()

        schema["endpoints"][endpoint_name] = {"method_count": len(method_names), "methods": {}}

        for method_name in method_names:
            method_info = api.get_method_info(endpoint_name, method_name)

            schema["endpoints"][endpoint_name]["methods"][method_name] = {
                "path": method_info["path"],
                "summary": method_info.get("summary", ""),
                "path_params": [p["name"] for p in method_info.get("path_params", [])],
                "query_params": [p["name"] for p in method_info.get("query_params", [])],
                "required_params": [
                    p["name"]
                    for p in method_info.get("path_params", [])
                    + method_info.get("query_params", [])
                    if p.get("required", False)
                ],
            }
            total_methods += 1

    schema["method_count"] = total_methods
    return schema


def export_etl_mapping():
    """Export ETL-specific mapping for data pipeline generation"""

    # This maps API methods to their likely materialized table structures
    etl_mapping = {
        "table_mappings": {
            # Game endpoint creates multiple tables
            "game": {
                "liveGameV1": {
                    "tables": ["game_live_data", "game_live_data_timecode"],
                    "primary_key": ["gamePk"],
                    "timecode_key": ["gamePk", "timecode"],
                    "partitioning": "by_date",
                },
                "boxscore": {
                    "tables": ["boxscores"],
                    "primary_key": ["gamePk"],
                    "partitioning": "by_date",
                },
                "linescore": {
                    "tables": ["linescores"],
                    "primary_key": ["gamePk"],
                    "partitioning": "by_date",
                },
                "playByPlay": {
                    "tables": ["play_by_play"],
                    "primary_key": ["gamePk"],
                    "partitioning": "by_date",
                },
            },
            # Team endpoint
            "team": {
                "teams": {"tables": ["teams"], "primary_key": ["teamId"], "type": "reference"},
                "roster": {
                    "tables": ["rosters"],
                    "primary_key": ["teamId", "rosterType"],
                    "type": "reference",
                },
                "stats": {
                    "tables": ["team_stats"],
                    "primary_key": ["teamId", "season", "statType"],
                    "partitioning": "by_season",
                },
            },
            # Person endpoint
            "person": {
                "person": {"tables": ["people"], "primary_key": ["personId"], "type": "reference"},
                "award": {
                    "tables": ["person_awards"],
                    "primary_key": ["personId", "awardId", "season"],
                    "type": "event",
                },
            },
            # Schedule endpoint
            "schedule": {
                "schedule": {
                    "tables": ["schedules"],
                    "primary_key": ["date", "sportId"],
                    "type": "event",
                    "partitioning": "by_date",
                }
            },
            # Stats endpoint
            "stats": {
                "stats": {
                    "tables": ["stats"],
                    "primary_key": ["group", "stats", "season", "sportId"],
                    "partitioning": "by_season",
                },
                "leaders": {
                    "tables": ["stat_leaders"],
                    "primary_key": ["leaderCategory", "season", "sportId"],
                    "partitioning": "by_season",
                },
            },
        },
        "ingestion_patterns": {
            "real_time": ["game.liveGameV1"],
            "hourly": ["game.liveGameV1 with timecode"],
            "daily": ["schedule.schedule", "stats.stats", "stats.leaders"],
            "weekly": ["team.teams", "team.roster", "person.person"],
            "seasonal": ["person.award", "draft.draftPicks"],
        },
        "relationships": {
            "season": ["schedule", "stats", "standings"],
            "schedule": ["game"],
            "game": ["team", "person", "boxscore", "linescore"],
            "team": ["person", "roster", "stats"],
            "person": ["stats", "awards"],
        },
    }

    return etl_mapping


def save_exports(output_dir="exports"):
    """Save all exports to files"""

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Export endpoint schema
    endpoint_schema = export_endpoint_schema()
    with open(output_path / "endpoint_schema.json", "w") as f:
        json.dump(endpoint_schema, f, indent=2)

    # Export ETL mapping
    etl_mapping = export_etl_mapping()
    with open(output_path / "etl_mapping.json", "w") as f:
        json.dump(etl_mapping, f, indent=2)

    print(f"Exported schema files to {output_path}/")
    print(
        f"- endpoint_schema.json: {endpoint_schema['method_count']} methods across {len(endpoint_schema['endpoints'])} endpoints"
    )
    print("- etl_mapping.json: Table mappings and ingestion patterns")

    return output_path


if __name__ == "__main__":
    save_exports()
