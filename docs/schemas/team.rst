Team Endpoint
=============

The ``team`` endpoint provides access to team-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **8 functional methods** and **2 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__leaders_base()
^^^^^^^^^^^^^^^^

**Summary:** View leaders for team stats

**Path:** ``/v1/teams/stats/leaders``

**Query Parameters:**

- ``leaderCategories`` (*array*, *optional*): TBD
- ``gameTypes`` (*array*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``stats`` (*array*, *optional*): Type of statistics. Format: Individual, Team, Career, etc. Available types in /api/v1/statTypes
- ``statType`` (*string*, *optional*): statType
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ... and 14 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View leaders for team stats
   response = api.Team.__leaders_base(leaderCategories="value", gameTypes="value", stats="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__leaders_teamId()
^^^^^^^^^^^^^^^^^^

**Summary:** View in

**Path:** ``/v1/teams/{teamId}/leaders``

**Path Parameters:**

- ``teamId`` (*integer*, **required**): teamId

**Query Parameters:**

- ``leaderCategories`` (*array*, *optional*): leaderCategories
- ``season`` (*string*, *optional*): season
- ``leaderGameTypes`` (*array*, *optional*): leaderGameTypes
- ``expand`` (*array*, *optional*): expands
- ``limit`` (*integer*, *optional*): limit
- ... and 3 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View in
   response = api.Team.__leaders_teamId(leaderCategories="value", season="2024", leaderGameTypes="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


alumni()
^^^^^^^^

**Summary:** View all team alumni

**Path:** ``/v1/teams/{teamId}/alumni``

**Path Parameters:**

- ``teamId`` (*integer*, **required**): Unique Team Identifier. Format: 141, 147, etc

**Query Parameters:**

- ``season`` (*string*, **required**): Season of play
- ``group`` (*string*, *optional*): Category of statistic to return. Available types in /api/v1/statGroups
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View all team alumni
   response = api.Team.alumni(season="2024", group="value", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


coaches()
^^^^^^^^^

**Summary:** View all coaches for a team

**Path:** ``/v1/teams/{teamId}/coaches``

**Path Parameters:**

- ``teamId`` (*integer*, **required**): Unique Team Identifier. Format: 141, 147, etc

**Query Parameters:**

- ``season`` (*string*, *optional*): Season of play
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View all coaches for a team
   response = api.Team.coaches(season="2024", date="2024-07-04", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


leaders()
^^^^^^^^^

**Summary:** View leaders for team stats

**Path:** ``/v1/teams/stats/leaders``

**Query Parameters:**

- ``leaderCategories`` (*array*, *optional*): TBD
- ``gameTypes`` (*array*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``stats`` (*array*, *optional*): Type of statistics. Format: Individual, Team, Career, etc. Available types in /api/v1/statTypes
- ``statType`` (*string*, *optional*): statType
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ... and 14 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View leaders for team stats
   response = api.Team.leaders(leaderCategories="value", gameTypes="value", stats="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


roster()
^^^^^^^^

**Summary:** View a teams info

**Path:** ``/v1/teams/{teamId}/roster/{rosterType}``

**Path Parameters:**

- ``teamId`` (*integer*, **required**): Unique Team Identifier. Format: 141, 147, etc
- ``rosterType`` (*Optional«string»*, **required**): Type of roster. Available types in /api/v1/rosterTypes

**Query Parameters:**

- ``season`` (*string*, *optional*): Season of play
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``gameType`` (*string*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a teams info
   response = api.Team.roster(season="2024", date="2024-07-04", gameType="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


stats()
^^^^^^^

**Summary:** View a teams stats

**Path:** ``/v1/teams/stats``

**Query Parameters:**

- ``gameType`` (*string*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ``stats`` (*array*, *optional*): Type of statistics. Format: Individual, Team, Career, etc. Available types in /api/v1/statTypes
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``sportIds`` (*array*, *optional*): Comma delimited list of top level organizations of a sport
- ``leagueIds`` (*array*, *optional*): Comma delimited list of Unique league identifiers
- ... and 13 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a teams stats
   response = api.Team.stats(gameType="value", stats="value", sportId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


teams()
^^^^^^^

**Summary:** View info for all teams

**Path:** ``/v1/teams``

**Query Parameters:**

- ``teamId`` (*Optional«int»*, *optional*): Unique Team Identifier. Format: 141, 147, etc
- ``season`` (*string*, *optional*): Season of play
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``divisionId`` (*integer*, *optional*): Unique Division Identifier
- ``gameType`` (*string*, *optional*): Type of Game. Available types in /api/v1/gameTypes
- ... and 6 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View info for all teams
   response = api.Team.teams(teamId=147, season="2024", sportId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Non-Functional Methods
--------------------------------------------------

.. warning::

   The following methods are **not functional** due to issues in the MLB Stats API or schema mismatches:

   - ``affiliates()``
   - ``allTeams()``

   These methods are excluded from the API and will not be available.


Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``team`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Team.get_method_names()
   print(methods)

   # Get method details
   method = api.Team.get_method('teams')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Team.describe_method('teams')
   print(description)
