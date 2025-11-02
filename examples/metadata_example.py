"""
Example showing how to use APIResponse metadata for custom storage/caching.

This demonstrates how consumers can:
1. Get complete metadata about requests and responses
2. Serialize everything to JSON for storage
3. Build custom storage keys from metadata
4. Store data in any backend (Redis, S3, filesystem, database, etc.)
"""

import json

from pymlb_statsapi.model.registry import StatsAPI


def main():
    # Make a request
    print("Fetching schedule data...")
    response = StatsAPI.Schedule.schedule(sportId=1, date="2024-07-04")

    # 1. Access just the data
    print("\n1. Just the data:")
    data = response.json()
    print(f"   Total games: {data.get('totalGames', 0)}")

    # 2. Get metadata only (no data payload)
    print("\n2. Metadata only:")
    metadata = response.get_metadata()
    print(f"   Request URL: {metadata['request']['url']}")
    print(f"   Status: {metadata['response']['status_code']}")
    print(f"   Response time: {metadata['response']['elapsed_ms']:.1f}ms")
    print(f"   Content size: {metadata['response']['content_length']} bytes")

    # 3. Get everything as a dict (metadata + data)
    print("\n3. Complete response as dict:")
    full_dict = response.to_dict()
    print(f"   Keys: {list(full_dict.keys())}")
    print(f"   Metadata keys: {list(full_dict['metadata'].keys())}")
    print(f"   Data preview: {str(full_dict['data'])[:100]}...")

    # 4. Save to JSON file (consumer's custom logic)
    print("\n4. Saving to custom locations:")

    # Example: Simple file storage
    filename = "schedule_2024-07-04.json"
    with open(filename, "w") as f:
        json.dump(full_dict, f, indent=2)
    print(f"   Saved to: {filename}")

    # Example: Build custom storage key from metadata
    req = metadata["request"]
    key = f"{req['domain']}:{req['endpoint_name']}:{req['method_name']}:{req['query_params']}"
    print(f"   Custom key: {key}")

    # Example: Store metadata separately
    metadata_filename = "schedule_2024-07-04_metadata.json"
    with open(metadata_filename, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"   Saved metadata to: {metadata_filename}")

    # Example: Get only metadata (no data)
    metadata_only_dict = response.to_dict(include_data=False)
    print(f"\n5. Metadata-only dict has 'data' key: {'data' in metadata_only_dict}")

    # Example: Build Redis key from metadata
    redis_key = f"mlb:{req['endpoint_name']}:{req['method_name']}:{json.dumps(req['query_params'], sort_keys=True)}"
    print(f"\n6. Redis key example: {redis_key}")

    # Example: Build S3 path from metadata
    s3_path = f"mlb-data/{req['endpoint_name']}/{req['method_name']}/date={req['query_params'].get('date')}/sportId={req['query_params'].get('sportId')}.json"
    print(f"\n7. S3 path example: {s3_path}")


if __name__ == "__main__":
    main()
