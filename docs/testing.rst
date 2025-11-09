Testing
=======

PyMLB StatsAPI has a comprehensive test suite combining unit tests (pytest) and behavior-driven development tests (behave).

Test Overview
-------------

- **30 unit tests** with pytest
- **39 BDD scenarios** covering all major endpoints
- **277 test steps** with path/query parameter variations
- **Stub-based testing** for fast, deterministic CI/CD
- **Real-world data** using completed games

Unit Tests
----------

Unit tests are written with pytest and located in ``tests/unit/``.

Running Unit Tests
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run all unit tests
   pytest

   # With coverage
   pytest --cov=pymlb_statsapi --cov-report=html

   # Specific test file
   pytest tests/unit/pymlb_statsapi/model/test_factory.py

   # Verbose output
   pytest -v

BDD Tests
---------

Behavior-driven development tests use behave framework with Gherkin feature files located in ``features/``.

Stub Capture/Replay System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The BDD tests support two modes:

1. **Replay mode** (default): Uses pre-captured API responses from gzipped JSON stubs
2. **Capture mode**: Makes real API calls and saves responses as stubs

This enables:

- Fast test execution (<1 second for full suite)
- Deterministic results in CI/CD
- No API rate limiting issues
- Ability to refresh stubs with real data

Running BDD Tests
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests with stubs (fast, default)
   behave

   # Or explicitly
   STUB_MODE=replay behave

   # Run specific feature
   behave features/schedule.feature

   # Verbose output
   behave -v features/season.feature

   # Test with specific tag
   behave --tags=@game

Capturing Fresh Stubs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Capture stubs by making real API calls
   STUB_MODE=capture behave

   # Capture stubs for specific endpoint
   STUB_MODE=capture behave features/schedule.feature

Stubs are saved to ``features/stubs/{endpoint}/{method}/`` as gzipped JSON files with parameter-based filenames.

Test Structure
--------------

Feature Files
~~~~~~~~~~~~~

Feature files define test scenarios in Gherkin syntax:

.. code-block:: gherkin

   Feature: Schedule API
     Scenario: Get schedule for a specific date
       Given the StatsAPI is available
       When I request schedule with parameters:
         | parameter | value      |
         | sportId   | 1          |
         | date      | 2024-10-27 |
       Then the response should be successful
       And the response should contain schedule data

Step Definitions
~~~~~~~~~~~~~~~~

Step definitions (in ``features/steps/``) implement the Gherkin steps using Python.

Stub Manager
~~~~~~~~~~~~

The ``StubManager`` class (``features/stub_manager.py``) handles:

- Generating consistent cache keys from API parameters
- Saving API responses as gzipped JSON
- Loading stubs during replay mode
- Managing stub file paths

Test Coverage
-------------

The test suite covers:

- All 21 MLB API endpoints
- Parameter validation
- Path and query parameter handling
- Response parsing
- Error handling
- File storage operations
- URI generation for multiple protocols

Running Tests in CI/CD
-----------------------

GitHub Actions workflow runs:

1. Unit tests with pytest (with coverage)
2. BDD tests in replay mode
3. Linting with ruff
4. Security scanning with bandit
5. Type checking with mypy

The test matrix includes:

- Python versions: 3.10, 3.11, 3.12, 3.13
- Operating systems: Ubuntu, macOS

All tests must pass before merging pull requests.
