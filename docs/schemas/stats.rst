Stats Endpoint
==============

The ``stats`` endpoint provides access to stats-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **3 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

groupedStats()
^^^^^^^^^^^^^^

**Summary:** View stats

**Path:** ``/v1/stats/grouped``

**Query Parameters:**

- ``stats`` (*array*, **required**): Type of statistics. Format: Individual, Team, Career, etc. Available types in /api/v1/statTypes
- ``personId`` (*integer*, *optional*): Unique Player Identifier. Format: 434538, 429665, etc
- ``teamId`` (*integer*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``teamIds`` (*array*, *optional*): Comma delimited list of Unique Team identifiers
- ``group`` (*array*, **required**): Category of statistic to return. Available types in /api/v1/statGroups
- ... and 30 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View stats
   response = api.Stats.groupedStats(stats="value", personId=1, teamId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


leaders()
^^^^^^^^^

**Summary:** Get leaders for a statistic

**Path:** ``/v1/stats/leaders``

**Query Parameters:**

- ``leaderCategories`` (*array*, *optional*): leaderCategories
- ``leaderGameTypes`` (*array*, *optional*): leaderGameTypes
- ``statGroup`` (*array*, *optional*): statGroup
- ``season`` (*string*, *optional*): season
- ``expand`` (*array*, *optional*): expands
- ... and 21 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get leaders for a statistic
   response = api.Stats.leaders(leaderCategories="value", leaderGameTypes="value", statGroup="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


stats()
^^^^^^^

**Summary:** View stats

**Path:** ``/v1/stats``

**Query Parameters:**

- ``stats`` (*array*, **required**): Type of statistics. Format: Individual, Team, Career, etc. Available types in /api/v1/statTypes
- ``personId`` (*integer*, *optional*): Unique Player Identifier. Format: 434538, 429665, etc
- ``teamId`` (*integer*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``teamIds`` (*array*, *optional*): Comma delimited list of Unique Team identifiers
- ``group`` (*array*, **required**): Category of statistic to return. Available types in /api/v1/statGroups
- ... and 28 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View stats
   response = api.Stats.stats(stats="value", personId=1, teamId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``stats`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Stats.get_method_names()
   print(methods)

   # Get method details
   method = api.Stats.get_method('stats')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Stats.describe_method('stats')
   print(description)
