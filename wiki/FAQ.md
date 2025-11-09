# Frequently Asked Questions

## General Questions

### What is PyMLB StatsAPI?

PyMLB StatsAPI is a fully schema-driven Python wrapper for the MLB Stats API. It provides a clean, Pythonic interface to access baseball statistics, game data, and more.

### Is this an official MLB product?

No, this is an independent open-source project. It wraps the MLB Stats API but is not affiliated with or endorsed by Major League Baseball.

### Is it free to use?

Yes! PyMLB StatsAPI is open-source under the MIT License. The underlying MLB Stats API is also free to use.

## Installation & Setup

### What Python versions are supported?

Python 3.10, 3.11, 3.12, and 3.13 on Linux, macOS, and Windows.

### How do I install it?

```bash
pip install pymlb-statsapi
```

For the latest development version:
```bash
pip install git+https://github.com/power-edge/pymlb_statsapi.git
```

### Do I need an API key?

No! The MLB Stats API is publicly accessible and doesn't require authentication.

## Usage

### Where can I find API examples?

- [Quick Start Guide](https://pymlb-statsapi.readthedocs.io/en/latest/quickstart.html)
- [Examples Page](https://pymlb-statsapi.readthedocs.io/en/latest/examples.html)
- [README.md](../README.md)

### How do I discover available endpoints and parameters?

```python
from pymlb_statsapi import api

# List all endpoints
endpoints = api.get_endpoint_names()

# Get methods for an endpoint
methods = api.Schedule.get_method_names()

# Get method documentation
print(api.Schedule.describe_method("schedule"))
```

### Can I save API responses?

Yes! All responses support saving as gzipped JSON with metadata:

```python
response = api.Schedule.schedule(sportId=1, date="2024-10-27")

# Save as gzipped JSON with metadata
result = response.gzip(prefix="mlb-data")
print(result['path'])  # File path
print(result['timestamp'])  # API call timestamp
```

## Development

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest` and `behave`
5. Submit a pull request

See [CLAUDE.md](../CLAUDE.md) for detailed development guidelines.

### How do I run tests?

```bash
# Unit tests
pytest

# BDD tests (with stubs)
behave tests/bdd/

# With coverage
pytest --cov=pymlb_statsapi
```

### How does the schema-driven approach work?

All endpoints and methods are dynamically generated from JSON schemas. There are no hardcoded model classes. This means:
- Automatic parameter validation
- Self-documenting API
- Easy updates when MLB changes their API

See [CLAUDE.md](../CLAUDE.md) for architecture details.

## Troubleshooting

### I'm getting import errors

Make sure you've installed the package:
```bash
pip install pymlb-statsapi
```

And you're importing correctly:
```python
from pymlb_statsapi import api  # Correct
# NOT: from pymlb_statsapi import StatsAPI
```

### API calls are failing

1. Check your internet connection
2. Verify the MLB Stats API is accessible: https://statsapi.mlb.com/api/v1/sports
3. Check the endpoint parameters against the schema

### Where do I report bugs?

Please [open an issue](https://github.com/power-edge/pymlb_statsapi/issues) on GitHub with:
- Python version
- Error message/traceback
- Minimal code to reproduce the issue

## More Help

- **Full Documentation**: https://pymlb-statsapi.readthedocs.io/
- **GitHub Issues**: https://github.com/power-edge/pymlb_statsapi/issues
- **GitHub Discussions**: https://github.com/power-edge/pymlb_statsapi/discussions
