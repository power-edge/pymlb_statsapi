League Endpoint
===============

The ``league`` endpoint provides access to league-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **4 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__allStarFinalVote_leagueId()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View league info

**Path:** ``/v1/leagues/{leagueId}/allStarFinalVote``

**Path Parameters:**

- ``leagueId`` (*Optional«int»*, **required**): leagueId

**Query Parameters:**

- ``season`` (*string*, *optional*): season
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View league info
   response = api.League.__allStarFinalVote_leagueId(season="2024", fields="value", leagueId=147)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__allStarWriteIns_leagueId()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View league info

**Path:** ``/v1/leagues/{leagueId}/allStarWriteIns``

**Path Parameters:**

- ``leagueId`` (*Optional«int»*, **required**): leagueId

**Query Parameters:**

- ``season`` (*string*, *optional*): season
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View league info
   response = api.League.__allStarWriteIns_leagueId(season="2024", fields="value", leagueId=147)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


allStarFinalVote()
^^^^^^^^^^^^^^^^^^

**Summary:** View league info

**Path:** ``/v1/league/{leagueId}/allStarFinalVote``

**Path Parameters:**

- ``leagueId`` (*Optional«int»*, **required**): leagueId

**Query Parameters:**

- ``season`` (*string*, *optional*): season
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View league info
   response = api.League.allStarFinalVote(season="2024", fields="value", leagueId=147)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


allStarWriteIns()
^^^^^^^^^^^^^^^^^

**Summary:** View league info

**Path:** ``/v1/league/{leagueId}/allStarWriteIns``

**Path Parameters:**

- ``leagueId`` (*Optional«int»*, **required**): leagueId

**Query Parameters:**

- ``season`` (*string*, *optional*): season
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View league info
   response = api.League.allStarWriteIns(season="2024", fields="value", leagueId=147)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``league`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.League.get_method_names()
   print(methods)

   # Get method details
   method = api.League.get_method('allStarFinalVote')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.League.describe_method('allStarFinalVote')
   print(description)
