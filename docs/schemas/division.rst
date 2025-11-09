Division Endpoint
=================

The ``division`` endpoint provides access to division-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **1 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

divisions()
^^^^^^^^^^^

**Summary:** Get division information

**Path:** ``/v1/divisions``

**Path Parameters:**

- ``divisionId`` (*Optional«int»*, **required**): Unique Division Identifier

**Query Parameters:**

- ``divisionId`` (*array*, *optional*): Comma delimited list of Unique League Identifiers
- ``includeInactive`` (*boolean*, *optional*): Whether or not to include inactive
- ``leagueId`` (*integer*, *optional*): Unique League Identifier
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``season`` (*string*, *optional*): Season of play
- ... and 1 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get division information
   response = api.Division.divisions(divisionId=147, includeInactive="value", leagueId=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``division`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Division.get_method_names()
   print(methods)

   # Get method details
   method = api.Division.get_method('divisions')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Division.describe_method('divisions')
   print(description)
