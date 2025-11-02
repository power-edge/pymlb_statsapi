Draft Endpoint
==============

The ``draft`` endpoint provides access to draft-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **3 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

draftPicks()
^^^^^^^^^^^^

**Summary:** View MLB Drafted Players

**Path:** ``/v1/draft``

**Path Parameters:**

- ``year`` (*Optional«int»*, **required**): Year the player was drafted. Format: 2000

**Query Parameters:**

- ``limit`` (*integer*, *optional*): Number of results to return
- ``offset`` (*integer*, *optional*): The pointer to start for a return set; used for pagination
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute
- ``order`` (*string*, *optional*): The order of sorting, ascending or descending
- ``sortBy`` (*string*, *optional*): Sort the set of data by the specified field
- ... and 11 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View MLB Drafted Players
   response = api.Draft.draftPicks(limit=1, offset=1, fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


draftProspects()
^^^^^^^^^^^^^^^^

**Summary:** View MLB Draft Prospects

**Path:** ``/v1/draft/prospects/{year}``

**Path Parameters:**

- ``year`` (*Optional«int»*, **required**): Year the player was drafted. Format: 2000

**Query Parameters:**

- ``limit`` (*integer*, *optional*): Number of results to return
- ``offset`` (*integer*, *optional*): The pointer to start for a return set; used for pagination
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute
- ``order`` (*string*, *optional*): The order of sorting, ascending or descending
- ``sortBy`` (*string*, *optional*): Sort the set of data by the specified field
- ... and 11 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View MLB Draft Prospects
   response = api.Draft.draftProspects(limit=1, offset=1, fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


latestDraftPicks()
^^^^^^^^^^^^^^^^^^

**Summary:** Get the last drafted player and the next 5 teams up to pick

**Path:** ``/v1/draft/{year}/latest``

**Path Parameters:**

- ``year`` (*Optional«int»*, **required**): Year the player was drafted. Format: 2000

**Query Parameters:**

- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get the last drafted player and the next 5 teams up to pick
   response = api.Draft.latestDraftPicks(fields="value", year="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``draft`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Draft.get_method_names()
   print(methods)

   # Get method details
   method = api.Draft.get_method('draftPicks')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Draft.describe_method('draftPicks')
   print(description)
