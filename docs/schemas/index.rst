Schema Reference
==================================================

**This is the core of PyMLB StatsAPI** - a comprehensive reference for all 21 MLB Stats API endpoints, automatically generated from JSON schemas.

Why Schemas Matter
--------------------------------------------------

Unlike traditional API wrappers with hardcoded methods, PyMLB StatsAPI dynamically generates **every endpoint and method** from JSON schemas. This means:

✅ **Zero hardcoding** - all methods are generated at runtime from schemas

✅ **Self-documenting** - schemas define parameters, types, and validation rules

✅ **Easy updates** - updating schemas automatically updates the entire API

✅ **Type-safe** - automatic parameter validation from schema definitions

.. note::

   These schemas were sourced from the MLB Stats API Beta documentation
   (https://beta-statsapi.mlb.com/docs/), which is no longer publicly available.

What You'll Find Here
--------------------------------------------------

Each endpoint page includes:

- **Overview** of functional and non-functional methods
- **Detailed parameter documentation** with types, required/optional flags, and descriptions
- **Working Python code examples** for every method
- **Schema introspection examples** showing how to explore the API programmatically
- **Clear warnings** for non-functional methods

.. toctree::
   :maxdepth: 1
   :caption: Endpoints

   awards
   broadcast
   conference
   config
   division
   draft
   game
   gamepace
   highlow
   homerunderby
   job
   league
   milestones
   person
   schedule
   season
   sports
   standings
   stats
   streaks
   team

Quick Reference
--------------------------------------------------

.. code-block:: python

   from pymlb_statsapi import api

   # List all available endpoints
   endpoints = api.get_endpoint_names()
   print(endpoints)

   # Get methods for an endpoint
   methods = api.Schedule.get_method_names()
   print(methods)

   # Get detailed info about a method
   info = api.get_method_info('schedule', 'schedule')
   print(info)
