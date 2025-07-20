# pymlb_statsapi
Python wrapper for MLB StatsAPI endpoints to get and save all data to your file system solution of choice.

# Example Usage

Getting a schedule. Passing date is optional, None will retrieve latest
```python
from pymlb_statsapi.model import StatsAPI

# Initialize the StatsAPI schedule object
sch = StatsAPI.Schedule.schedule(query_params={"sportId": 1, "date": "2025-06-01"})

sch.get()  # also returns self with data

# Save to file system
gz = sch.gzip()

endpoint_name = sch.endpoint.get_name()

print("saved %s data to %s" % (
    endpoint_name,
    gz["path"]
))


# use your provider to manage the data
import boto3

s3 = boto3.client("s3")

key = f"data/{sch.domain}/{sch.prefix()}"

s3.upload_file(
    Filename=gz["path"],
    Bucket="my-pymlb-statsapi-bucket",
    Key=key
)
```

# Config Driven

This library is config driven. Endpoints, API methods, and parameters are all mapped to the `pymlb_statsapi/resources/`.
