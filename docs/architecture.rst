Architecture
============

PyMLB StatsAPI uses a config-driven, schema-based architecture where all MLB API endpoints are defined as JSON schemas rather than hardcoded Python classes.

Core Design Pattern
-------------------

**Schema-Driven API Wrapper**

The library uses JSON schemas to define MLB API endpoints, enabling:

- Dynamic endpoint discovery
- Self-documenting API methods
- Easy updates when MLB API changes
- Automatic parameter validation

Key Components
--------------

Schema System
~~~~~~~~~~~~~

Located in ``pymlb_statsapi/resources/schemas/``:

- ``endpoint-model.json``: Master configuration mapping endpoint names to paths and method names
- ``schemas/statsapi/stats_api_1_0/*.json``: Individual endpoint schemas with full parameter definitions

Each JSON schema defines:

- Available operations (methods)
- Parameters (path vs query)
- Validation rules
- Documentation

Model Layer
~~~~~~~~~~~

**Base Models** (``model/factory.py``):

- ``DynamicEndpoint``: Base class for all endpoint models
- ``EndpointMethod``: Represents individual API operations
- ``APIResponse``: Response wrapper with metadata

**Dynamic Factory** (``model/factory.py``):

- Generates endpoint classes and methods from schemas at runtime
- Creates clean function signatures with proper parameter handling
- Handles method overloading

**Registry** (``model/registry.py``):

- Central ``api`` singleton that loads all endpoints
- Provides discovery API for exploring available methods

Clean API Pattern
~~~~~~~~~~~~~~~~~

The "Clean API" intelligently routes parameters to path or query parameters based on each method's schema configuration. Developers simply pass parameters as keyword arguments:

.. code-block:: python

   # Library automatically determines parameter types from schema
   response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
   # Resolves to: /api/v1/game/747175/feed/live?timecode=20241027_000000

Data Flow
---------

1. User calls ``api.Schedule.schedule(sportId=1, date="2025-06-01")``
2. Registry returns ``ScheduleModel`` instance (loaded from schedule.json schema)
3. ``.schedule()`` method looks up configuration in endpoint-model.json
4. Returns ``APIResponse`` with:

   - Endpoint model
   - API definition from schema
   - Operation with parameter rules
   - Resolved URL: ``https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-06-01``

5. Response includes ``.json()``, ``.save_json()``, ``.get_uri()`` methods

Configuration
-------------

The architecture is controlled by:

- ``endpoint-model.json``: Endpoint to path mappings
- Individual schema files: Operation definitions and parameter rules
- Environment variables: ``PYMLB_STATSAPI__BASE_FILE_PATH``, etc.

This design enables the library to adapt to MLB API changes by simply updating JSON schemas, with no code modifications required.
