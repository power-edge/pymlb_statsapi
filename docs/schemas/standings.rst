Standings Endpoint
==================

The ``standings`` endpoint provides access to standings-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **1 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

standings()
^^^^^^^^^^^

**Summary:** View standings for a league

**Path:** ``/v1/standings/{standingsType}``

**Path Parameters:**

- ``standingsType`` (*Optional«string»*, **required**): Type of season. Available types in /api/v1/standingsTypes

**Query Parameters:**

- ``leagueId`` (*array*, *optional*): Unique League Identifier
- ``season`` (*string*, *optional*): Season of play
- ``standingsType`` (*string*, *optional*): Type of season. Available types in /api/v1/standingsTypes
- ``standingsTypes`` (*array*, *optional*): Type of season. Available types in /api/v1/standingsTypes
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ... and 4 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View standings for a league
   response = api.Standings.standings(leagueId=147, season="2024", standingsType="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``standings`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Standings.get_method_names()
   print(methods)

   # Get method details
   method = api.Standings.get_method('standings')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Standings.describe_method('standings')
   print(description)
