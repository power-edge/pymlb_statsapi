Broadcast Endpoint
==================

The ``broadcast`` endpoint provides access to broadcast-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **1 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

getBroadcasts()
^^^^^^^^^^^^^^^

**Summary:** getBroadcasts

**Path:** ``/v1/broadcast``

**Query Parameters:**

- ``broadcasterIds`` (*array*, **required**): All of the broadcast details
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # getBroadcasts
   response = api.Broadcast.getBroadcasts(broadcasterIds="value", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``broadcast`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Broadcast.get_method_names()
   print(methods)

   # Get method details
   method = api.Broadcast.get_method('getBroadcasts')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Broadcast.describe_method('getBroadcasts')
   print(description)
