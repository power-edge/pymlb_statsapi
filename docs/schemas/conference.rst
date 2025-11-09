Conference Endpoint
===================

The ``conference`` endpoint provides access to conference-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **1 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

conferences()
^^^^^^^^^^^^^

**Summary:** View conference info

**Path:** ``/v1/conferences``

**Path Parameters:**

- ``conferenceId`` (*Optional«int»*, **required**): conferenceId

**Query Parameters:**

- ``conferenceId`` (*array*, *optional*): conferenceIds
- ``season`` (*string*, *optional*): season
- ``includeInactive`` (*boolean*, *optional*): includeInactive
- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View conference info
   response = api.Conference.conferences(conferenceId=147, season="2024", includeInactive="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``conference`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Conference.get_method_names()
   print(methods)

   # Get method details
   method = api.Conference.get_method('conferences')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Conference.describe_method('conferences')
   print(description)
