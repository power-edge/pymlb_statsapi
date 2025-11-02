Season Endpoint
===============

The ``season`` endpoint provides access to season-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **4 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__seasons_base()
^^^^^^^^^^^^^^^^

**Summary:** View season info

**Path:** ``/v1/seasons``

**Query Parameters:**

- ``seasonId`` (*Optional«string»*, *optional*): Season of play
- ``season`` (*array*, *optional*): Season of play
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``withGameTypeDates`` (*boolean*, *optional*): Retrieve dates for each game type
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View season info
   response = api.Season.__seasons_base(seasonId=147, season="2024", sportId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__seasons_seasonId()
^^^^^^^^^^^^^^^^^^^^

**Summary:** View season info

**Path:** ``/v1/seasons/{seasonId}``

**Path Parameters:**

- ``seasonId`` (*Optional«string»*, **required**): Season of play

**Query Parameters:**

- ``season`` (*array*, *optional*): Season of play
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``withGameTypeDates`` (*boolean*, *optional*): Retrieve dates for each game type
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View season info
   response = api.Season.__seasons_seasonId(season="2024", sportId=1, withGameTypeDates="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


allSeasons()
^^^^^^^^^^^^

**Summary:** View all seasons

**Path:** ``/v1/seasons/all``

**Query Parameters:**

- ``divisionId`` (*integer*, *optional*): Unique Division Identifier
- ``leagueId`` (*integer*, *optional*): Unique League Identifier
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``withGameTypeDates`` (*boolean*, *optional*): Retrieve dates for each game type
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View all seasons
   response = api.Season.allSeasons(divisionId=1, leagueId=1, sportId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


seasons()
^^^^^^^^^

**Summary:** View season info

**Path:** ``/v1/seasons``

**Query Parameters:**

- ``seasonId`` (*Optional«string»*, *optional*): Season of play
- ``season`` (*array*, *optional*): Season of play
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``withGameTypeDates`` (*boolean*, *optional*): Retrieve dates for each game type
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View season info
   response = api.Season.seasons(seasonId=147, season="2024", sportId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``season`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Season.get_method_names()
   print(methods)

   # Get method details
   method = api.Season.get_method('seasons')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Season.describe_method('seasons')
   print(description)
