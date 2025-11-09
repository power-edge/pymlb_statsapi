Config Endpoint
===============

The ``config`` endpoint provides access to config-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **36 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

aggregateSortEnum()
^^^^^^^^^^^^^^^^^^^

**Summary:** List all stat fields

**Path:** ``/v1/sortModifiers``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all stat fields
   response = api.Config.aggregateSortEnum()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


awards()
^^^^^^^^

**Summary:** List all awards

**Path:** ``/v1/awards``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all awards
   response = api.Config.awards()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


baseballStats()
^^^^^^^^^^^^^^^

**Summary:** List all baseball stats

**Path:** ``/v1/baseballStats``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all baseball stats
   response = api.Config.baseballStats()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


eventTypes()
^^^^^^^^^^^^

**Summary:** List all event types

**Path:** ``/v1/eventTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all event types
   response = api.Config.eventTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


fielderDetailTypes()
^^^^^^^^^^^^^^^^^^^^

**Summary:** List fielder detail types

**Path:** ``/v1/fielderDetailTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List fielder detail types
   response = api.Config.fielderDetailTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


gameStatus()
^^^^^^^^^^^^

**Summary:** List all status types

**Path:** ``/v1/gameStatus``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all status types
   response = api.Config.gameStatus()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


gameTypes()
^^^^^^^^^^^

**Summary:** List all game types

**Path:** ``/v1/gameTypes``

**Query Parameters:**

- ``sportId`` (*integer*, *optional*): sportId
- ``leagueId`` (*integer*, *optional*): leagueId
- ``season`` (*string*, *optional*): season

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all game types
   response = api.Config.gameTypes(sportId=1, leagueId=1, season="2024")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


gamedayTypes()
^^^^^^^^^^^^^^

**Summary:** List all hit trajectories

**Path:** ``/v1/gamedayTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all hit trajectories
   response = api.Config.gamedayTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


groupByTypes()
^^^^^^^^^^^^^^

**Summary:** List groupBy types

**Path:** ``/v1/groupByTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List groupBy types
   response = api.Config.groupByTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


hitTrajectories()
^^^^^^^^^^^^^^^^^

**Summary:** List all hit trajectories

**Path:** ``/v1/hitTrajectories``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all hit trajectories
   response = api.Config.hitTrajectories(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


jobTypes()
^^^^^^^^^^

**Summary:** List all job types

**Path:** ``/v1/jobTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all job types
   response = api.Config.jobTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


languages()
^^^^^^^^^^^

**Summary:** List all support languages

**Path:** ``/v1/languages``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all support languages
   response = api.Config.languages()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


leagueLeaderTypes()
^^^^^^^^^^^^^^^^^^^

**Summary:** List all possible player league leader types

**Path:** ``/v1/leagueLeaderTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all possible player league leader types
   response = api.Config.leagueLeaderTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


logicalEvents()
^^^^^^^^^^^^^^^

**Summary:** List all logical event types

**Path:** ``/v1/logicalEvents``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all logical event types
   response = api.Config.logicalEvents(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


metrics()
^^^^^^^^^

**Summary:** List all possible metrics

**Path:** ``/v1/metrics``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all possible metrics
   response = api.Config.metrics()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


pitchCodes()
^^^^^^^^^^^^

**Summary:** List all pitch codes

**Path:** ``/v1/pitchCodes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all pitch codes
   response = api.Config.pitchCodes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


pitchTypes()
^^^^^^^^^^^^

**Summary:** List all pitch classification types

**Path:** ``/v1/pitchTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all pitch classification types
   response = api.Config.pitchTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


platforms()
^^^^^^^^^^^

**Summary:** List all possible platforms

**Path:** ``/v1/platforms``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all possible platforms
   response = api.Config.platforms()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


playerStatusCodes()
^^^^^^^^^^^^^^^^^^^

**Summary:** List all player status codes

**Path:** ``/v1/playerStatusCodes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all player status codes
   response = api.Config.playerStatusCodes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


positions()
^^^^^^^^^^^

**Summary:** List all possible positions

**Path:** ``/v1/positions``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all possible positions
   response = api.Config.positions()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


reviewReasons()
^^^^^^^^^^^^^^^

**Summary:** List all replay review reasons

**Path:** ``/v1/reviewReasons``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all replay review reasons
   response = api.Config.reviewReasons(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


rosterTypes()
^^^^^^^^^^^^^

**Summary:** List all possible roster types

**Path:** ``/v1/rosterTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all possible roster types
   response = api.Config.rosterTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


runnerDetailTypes()
^^^^^^^^^^^^^^^^^^^

**Summary:** List runner detail types

**Path:** ``/v1/runnerDetailTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List runner detail types
   response = api.Config.runnerDetailTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


scheduleEventTypes()
^^^^^^^^^^^^^^^^^^^^

**Summary:** List all event types

**Path:** ``/v1/scheduleEventTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all event types
   response = api.Config.scheduleEventTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


sitCodes()
^^^^^^^^^^

**Summary:** List all situation codes

**Path:** ``/v1/situationCodes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute
- ``season`` (*string*, *optional*): season
- ``statGroup`` (*string*, *optional*): statGroup

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all situation codes
   response = api.Config.sitCodes(fields="value", season="2024", statGroup="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


sky()
^^^^^

**Summary:** List all sky options

**Path:** ``/v1/sky``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all sky options
   response = api.Config.sky(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


standingsTypes()
^^^^^^^^^^^^^^^^

**Summary:** List all standings types

**Path:** ``/v1/standingsTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all standings types
   response = api.Config.standingsTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statFields()
^^^^^^^^^^^^

**Summary:** List all stat fields

**Path:** ``/v1/statFields``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all stat fields
   response = api.Config.statFields()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statGroups()
^^^^^^^^^^^^

**Summary:** List all stat groups

**Path:** ``/v1/statGroups``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all stat groups
   response = api.Config.statGroups()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statSearchConfig()
^^^^^^^^^^^^^^^^^^

**Summary:** Stats Search Config Endpoint

**Path:** ``/v1/stats/search/config``

**Query Parameters:**

- ``filterLevel`` (*string*, *optional*): inputFilterLevel
- ``group`` (*string*, *optional*): inputStatGroup

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Stats Search Config Endpoint
   response = api.Config.statSearchConfig(filterLevel="value", group="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statSearchGroupByTypes()
^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** List groupBy types

**Path:** ``/v1/stats/search/groupByTypes``

**Query Parameters:**

- ``filterLevel`` (*string*, *optional*): filterLevel

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List groupBy types
   response = api.Config.statSearchGroupByTypes(filterLevel="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statSearchParams()
^^^^^^^^^^^^^^^^^^

**Summary:** List stat search parameters

**Path:** ``/v1/stats/search/params``

**Query Parameters:**

- ``filterLevel`` (*string*, *optional*): filterLevel

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List stat search parameters
   response = api.Config.statSearchParams(filterLevel="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statSearchStats()
^^^^^^^^^^^^^^^^^

**Summary:** List stat search stats

**Path:** ``/v1/stats/search/stats``

**Query Parameters:**

- ``filterLevel`` (*string*, *optional*): filterLevel

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List stat search stats
   response = api.Config.statSearchStats(filterLevel="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


statTypes()
^^^^^^^^^^^

**Summary:** List all stat types

**Path:** ``/v1/statTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all stat types
   response = api.Config.statTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


transactionTypes()
^^^^^^^^^^^^^^^^^^

**Summary:** List all hit trajectories

**Path:** ``/v1/transactionTypes``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all hit trajectories
   response = api.Config.transactionTypes(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


windDirection()
^^^^^^^^^^^^^^^

**Summary:** List all wind direction options

**Path:** ``/v1/windDirection``

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # List all wind direction options
   response = api.Config.windDirection(fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``config`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Config.get_method_names()
   print(methods)

   # Get method details
   method = api.Config.get_method('baseballStats')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Config.describe_method('baseballStats')
   print(description)
