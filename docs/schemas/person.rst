Person Endpoint
===============

The ``person`` endpoint provides access to person-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **7 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__currentGameStats_base()
^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a players change log

**Path:** ``/v1/people/changes``

**Query Parameters:**

- ``updatedSince`` (*string*, **required**): Format: YYYY-MM-DDTHH:MM:SSZ
- ``limit`` (*integer*, *optional*): Number of results to return
- ``offset`` (*integer*, *optional*): The pointer to start for a return set; used for pagination
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players change log
   response = api.Person.__currentGameStats_base(updatedSince="value", limit=1, offset=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__currentGameStats_personId()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a players stats

**Path:** ``/v1/people/{personId}/stats/game/current``

**Path Parameters:**

- ``personId`` (*integer*, **required**): Unique Player Identifier. Format: 434538, 429665, etc

**Query Parameters:**

- ``group`` (*array*, *optional*): Category of statistic to return. Available types in /api/v1/statGroups
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players stats
   response = api.Person.__currentGameStats_personId(group="value", fields="value", personId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__currentGameStats_personId_gamePk()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a players stats

**Path:** ``/v1/people/{personId}/stats/game/{gamePk}``

**Path Parameters:**

- ``personId`` (*integer*, **required**): Unique Player Identifier. Format: 434538, 429665, etc
- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``group`` (*array*, *optional*): Category of statistic to return. Available types in /api/v1/statGroups
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players stats
   response = api.Person.__currentGameStats_personId_gamePk(group="value", fields="value", personId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


award()
^^^^^^^

**Summary:** View a players awards

**Path:** ``/v1/people/{personId}/awards``

**Path Parameters:**

- ``personId`` (*integer*, **required**): personId

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players awards
   response = api.Person.award(fields="value", personId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


currentGameStats()
^^^^^^^^^^^^^^^^^^

**Summary:** View a players change log

**Path:** ``/v1/people/changes``

**Query Parameters:**

- ``updatedSince`` (*string*, **required**): Format: YYYY-MM-DDTHH:MM:SSZ
- ``limit`` (*integer*, *optional*): Number of results to return
- ``offset`` (*integer*, *optional*): The pointer to start for a return set; used for pagination
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players change log
   response = api.Person.currentGameStats(updatedSince="value", limit=1, offset=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


freeAgents()
^^^^^^^^^^^^

**Summary:** freeAgents

**Path:** ``/v1/people/freeAgents``

**Query Parameters:**

- ``season`` (*string*, **required**): Season of play
- ``order`` (*string*, *optional*): The order of sorting, ascending or descending
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # freeAgents
   response = api.Person.freeAgents(season="2024", order="value", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


person()
^^^^^^^^

**Summary:** View a players stats

**Path:** ``/v1/people``

**Query Parameters:**

- ``personIds`` (*array*, *optional*): Comma delimited list of person ID. Format: 1234, 2345
- ``season`` (*string*, *optional*): Season of play
- ``group`` (*array*, *optional*): Category of statistic to return. Available types in /api/v1/statGroups
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a players stats
   response = api.Person.person(personIds="value", season="2024", group="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``person`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Person.get_method_names()
   print(methods)

   # Get method details
   method = api.Person.get_method('person')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Person.describe_method('person')
   print(description)
