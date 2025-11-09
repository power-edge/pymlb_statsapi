Game Endpoint
=============

The ``game`` endpoint provides access to game-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **12 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

boxscore()
^^^^^^^^^^

**Summary:** Get game boxscore.

**Path:** ``/v1/game/{game_pk}/boxscore``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get game boxscore.
   response = api.Game.boxscore(timecode="value", fields="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


colorFeed()
^^^^^^^^^^^

**Summary:** Get game color feed.

**Path:** ``/v1/game/{game_pk}/feed/color``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get game color feed.
   response = api.Game.colorFeed(timecode="value", fields="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


colorTimestamps()
^^^^^^^^^^^^^^^^^

**Summary:** Retrieve all of the color timestamps for a game.

**Path:** ``/v1/game/{game_pk}/feed/color/timestamps``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Retrieve all of the color timestamps for a game.
   response = api.Game.colorTimestamps(game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


content()
^^^^^^^^^

**Summary:** Retrieve all content for a game.

**Path:** ``/v1/game/{game_pk}/content``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): gamePk

**Query Parameters:**

- ``highlightLimit`` (*integer*, *optional*): Number of results to return

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Retrieve all content for a game.
   response = api.Game.content(highlightLimit=1, game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


currentGameStats()
^^^^^^^^^^^^^^^^^^

**Summary:** View a game change log

**Path:** ``/v1/game/changes``

**Query Parameters:**

- ``updatedSince`` (*string*, **required**): Format: YYYY-MM-DDTHH:MM:SSZ
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``sportIds`` (*array*, *optional*): Comma delimited list of top level organizations of a sport
- ``gameType`` (*string*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``gameTypes`` (*array*, *optional*): Comma delimited list of type of Game. Available types in /api/v1/gameTypes
- ... and 4 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a game change log
   response = api.Game.currentGameStats(updatedSince="value", sportId=1, sportIds="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


getGameContextMetrics()
^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** Get the context metrics for this game based on its current state

**Path:** ``/v1/game/{gamePk}/contextMetrics``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get the context metrics for this game based on its current state
   response = api.Game.getGameContextMetrics(timecode="value", fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


getWinProbability()
^^^^^^^^^^^^^^^^^^^

**Summary:** Get the win probability for this game

**Path:** ``/v1/game/{gamePk}/winProbability``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get the win probability for this game
   response = api.Game.getWinProbability(timecode="value", fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


linescore()
^^^^^^^^^^^

**Summary:** Get game linescore

**Path:** ``/v1/game/{game_pk}/linescore``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get game linescore
   response = api.Game.linescore(timecode="value", fields="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


liveGameDiffPatchV1()
^^^^^^^^^^^^^^^^^^^^^

**Summary:** Get live game status.

**Path:** ``/v1.1/game/{game_pk}/feed/live/diffPatch``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``startTimecode`` (*string*, *optional*): Start time code will give you everything since that time. Format: MMDDYYYY_HHMMSS
- ``endTimecode`` (*string*, *optional*): End time code will give you a snapshot at that specific time. Format: MMDDYYYY_HHMMSS

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get live game status.
   response = api.Game.liveGameDiffPatchV1(startTimecode="value", endTimecode="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


liveGameV1()
^^^^^^^^^^^^

**Summary:** Get live game status.

**Path:** ``/v1.1/game/{game_pk}/feed/live``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get live game status.
   response = api.Game.liveGameV1(timecode="value", fields="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


liveTimestampv11()
^^^^^^^^^^^^^^^^^^

**Summary:** Retrieve all of the play timestamps for a game.

**Path:** ``/v1.1/game/{game_pk}/feed/live/timestamps``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Retrieve all of the play timestamps for a game.
   response = api.Game.liveTimestampv11(game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


playByPlay()
^^^^^^^^^^^^

**Summary:** Get game play By Play

**Path:** ``/v1/game/{game_pk}/playByPlay``

**Path Parameters:**

- ``game_pk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``timecode`` (*string*, *optional*): Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get game play By Play
   response = api.Game.playByPlay(timecode="value", fields="value", game_pk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``game`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Game.get_method_names()
   print(methods)

   # Get method details
   method = api.Game.get_method('liveGameV1')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Game.describe_method('liveGameV1')
   print(description)
