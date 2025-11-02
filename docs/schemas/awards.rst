Awards Endpoint
===============

The ``awards`` endpoint provides access to awards-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **2 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

awardRecipients()
^^^^^^^^^^^^^^^^^

**Summary:** View recipients of an award

**Path:** ``/v1/awards/{awardId}/recipients``

**Path Parameters:**

- ``awardId`` (*string*, **required**): Unique Award Identifier. Available awards in /api/v1/awards

**Query Parameters:**

- ``season`` (*string*, *optional*): Season of play
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``leagueId`` (*array*, *optional*): Comma delimited list of Unique league identifiers
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View recipients of an award
   response = api.Awards.awardRecipients(season="2024", sportId=1, leagueId=147)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


awards()
^^^^^^^^

**Summary:** View awards info

**Path:** ``/v1/awards/{awardId}``

**Path Parameters:**

- ``awardId`` (*Optional«string»*, **required**): Unique Award Identifier. Available awards in /api/v1/awards

**Query Parameters:**

- ``awardId`` (*array*, *optional*): Comma delimited list of Unique Award Identifier. Available awards in /api/v1/awards
- ``orgId`` (*array*, *optional*): Comma delimited list of top level organizations of a sport
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View awards info
   response = api.Awards.awards(awardId=147, orgId=147, fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``awards`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Awards.get_method_names()
   print(methods)

   # Get method details
   method = api.Awards.get_method('awards')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Awards.describe_method('awards')
   print(description)
