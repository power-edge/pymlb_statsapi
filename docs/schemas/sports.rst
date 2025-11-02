Sports Endpoint
===============

The ``sports`` endpoint provides access to sports-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **1 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

sportPlayers()
^^^^^^^^^^^^^^

**Summary:** Get all players for a sport level

**Path:** ``/v1/sports/{sportId}/players``

**Path Parameters:**

- ``sportId`` (*Optional«int»*, **required**): Top level organization of a sport

**Query Parameters:**

- ``season`` (*Optional«string»*, *optional*): Season of play
- ``gameType`` (*string*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``hasStats`` (*boolean*, *optional*): Returns sports that have individual player stats

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get all players for a sport level
   response = api.Sports.sportPlayers(season="2024", gameType="value", hasStats="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``sports`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Sports.get_method_names()
   print(methods)

   # Get method details
   method = api.Sports.get_method('sportPlayers')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Sports.describe_method('sportPlayers')
   print(description)
