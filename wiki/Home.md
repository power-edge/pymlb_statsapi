# PyMLB StatsAPI Wiki

Welcome to the PyMLB StatsAPI wiki! This is a quick reference guide that links to our comprehensive documentation.

## 📚 Documentation

For complete documentation, please visit:

**[PyMLB StatsAPI Documentation on ReadTheDocs →](https://pymlb-statsapi.readthedocs.io/)**

## 🚀 Quick Links

### Getting Started
- **[README](../README.md)** - Project overview, installation, and quick start
- **[Installation Guide](https://pymlb-statsapi.readthedocs.io/en/latest/installation.html)** - Detailed installation instructions
- **[Quick Start Tutorial](https://pymlb-statsapi.readthedocs.io/en/latest/quickstart.html)** - Get up and running in minutes

### Development
- **[CLAUDE.md](../CLAUDE.md)** - Development guide and project architecture
- **[RELEASE.md](../RELEASE.md)** - Release process and CI/CD workflow
- **[CONTRIBUTORS](../CONTRIBUTORS)** - Contribution guidelines and authorship

### API Reference
- **[API Documentation](https://pymlb-statsapi.readthedocs.io/en/latest/api.html)** - Complete API reference
- **[Examples](https://pymlb-statsapi.readthedocs.io/en/latest/examples.html)** - Code examples and recipes

## 📦 Installation

```bash
pip install pymlb-statsapi
```

## 💡 Quick Example

```python
from pymlb_statsapi import api

# Get today's schedule
schedule = api.Schedule.schedule(sportId=1, date="2024-10-27")
print(schedule.json())

# Get live game data
game = api.Game.liveGameV1(game_pk="747175")
print(game.json())
```

## 🔗 External Resources

- **[PyPI Package](https://pypi.org/project/pymlb-statsapi/)** - Install via pip
- **[GitHub Repository](https://github.com/power-edge/pymlb_statsapi)** - Source code and issues
- **[GitHub Actions](https://github.com/power-edge/pymlb_statsapi/actions)** - CI/CD status
- **[Codecov](https://codecov.io/gh/power-edge/pymlb_statsapi)** - Code coverage reports

## 🤝 Contributing

We welcome contributions! Please see:
- **[Issues](https://github.com/power-edge/pymlb_statsapi/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/power-edge/pymlb_statsapi/discussions)** - Questions and ideas
- **[Pull Requests](https://github.com/power-edge/pymlb_statsapi/pulls)** - Code contributions

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Note**: This wiki provides quick links. For detailed documentation, always refer to [ReadTheDocs](https://pymlb-statsapi.readthedocs.io/).
