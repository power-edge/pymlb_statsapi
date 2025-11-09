Schedule Endpoint
=================

The ``schedule`` endpoint provides access to schedule-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **6 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__schedule_base()
^^^^^^^^^^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule``

**Query Parameters:**

- ``calendarTypes`` (*array*, *optional*): Comma delimited list of type of calendar types
- ``eventTypes`` (*array*, *optional*): Comma delimited list of type of events. <b>Note: Don't Use. This will be deprecated in favor of calendarTypes</b>
- ``scheduleEventTypes`` (*array*, *optional*): Comma delimited list of type of event types
- ``teamId`` (*array*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``leagueId`` (*array*, *optional*): Unique League Identifier
- ... and 18 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.__schedule_base(calendarTypes="value", eventTypes="value", scheduleEventTypes="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__schedule_scheduleType()
^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule/{scheduleType}``

**Query Parameters:**

- ``calendarTypes`` (*array*, *optional*): Comma delimited list of type of calendar types
- ``eventTypes`` (*array*, *optional*): Comma delimited list of type of events. <b>Note: Don't Use. This will be deprecated in favor of calendarTypes</b>
- ``scheduleEventTypes`` (*array*, *optional*): Comma delimited list of type of event types
- ``teamId`` (*array*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``leagueId`` (*array*, *optional*): Unique League Identifier
- ... and 18 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.__schedule_scheduleType(calendarTypes="value", eventTypes="value", scheduleEventTypes="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


postseasonScheduleSeries()
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule/postseason/series``

**Query Parameters:**

- ``gameTypes`` (*array*, *optional*): Comma delimited list of type of Game. Available types in /api/v1/gameTypes
- ``seriesNumber`` (*integer*, *optional*): seriesNumber
- ``teamId`` (*integer*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``sportId`` (*integer*, *optional*): Unique League Identifier
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ... and 6 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.postseasonScheduleSeries(gameTypes="value", seriesNumber=1, teamId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


schedule()
^^^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule``

**Query Parameters:**

- ``calendarTypes`` (*array*, *optional*): Comma delimited list of type of calendar types
- ``eventTypes`` (*array*, *optional*): Comma delimited list of type of events. <b>Note: Don't Use. This will be deprecated in favor of calendarTypes</b>
- ``scheduleEventTypes`` (*array*, *optional*): Comma delimited list of type of event types
- ``teamId`` (*array*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``leagueId`` (*array*, *optional*): Unique League Identifier
- ... and 18 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.schedule(calendarTypes="value", eventTypes="value", scheduleEventTypes="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


tieGames()
^^^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule/games/tied``

**Query Parameters:**

- ``sportId`` (*array*, *optional*): Top level organization of a sport
- ``gameTypes`` (*array*, *optional*): Comma delimited list of type of Game. Available types in /api/v1/gameTypes
- ``season`` (*string*, **required**): Season of play
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.tieGames(sportId=147, gameTypes="value", season="2024")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


tuneIn()
^^^^^^^^

**Summary:** View schedule info

**Path:** ``/v1/schedule/postseason/tuneIn``

**Query Parameters:**

- ``teamId`` (*integer*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``sportId`` (*integer*, *optional*): Unique League Identifier
- ``season`` (*string*, *optional*): Unique Primary Key Representing a Game
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View schedule info
   response = api.Schedule.tuneIn(teamId=1, sportId=1, season="2024")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``schedule`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Schedule.get_method_names()
   print(methods)

   # Get method details
   method = api.Schedule.get_method('schedule')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Schedule.describe_method('schedule')
   print(description)
