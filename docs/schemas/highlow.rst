Highlow Endpoint
================

The ``highlow`` endpoint provides access to highlow-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **2 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

highLow()
^^^^^^^^^

**Summary:** View high/low stats by player or team

**Path:** ``/v1/highLow/types``

**Path Parameters:**

- ``highLowType`` (*string*, **required**): Type of high/low stats ('player', 'team', 'game')

**Query Parameters:**

- ``statGroup`` (*array*, *optional*): Comma delimited list of  categories of statistic to return. Available types in /api/v1/statGroups
- ``sortStat`` (*array*, *optional*): Comma delimited list of baseball stats to sort splits by.
- ``season`` (*array*, *optional*): Comma delimited list of Seasons of play
- ``gameType`` (*array*, *optional*): Comma delimited list of type of Game. Available types in /api/v1/gameTypes
- ``teamId`` (*integer*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ... and 5 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View high/low stats by player or team
   response = api.Highlow.highLow(statGroup="value", sortStat="value", season="2024")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


highLowStats()
^^^^^^^^^^^^^^

**Summary:** View high/low stat types

**Path:** ``/v1/highLow/{highLowType}``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View high/low stat types
   response = api.Highlow.highLowStats()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``highlow`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Highlow.get_method_names()
   print(methods)

   # Get method details
   method = api.Highlow.get_method('highLowStats')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Highlow.describe_method('highLowStats')
   print(description)
