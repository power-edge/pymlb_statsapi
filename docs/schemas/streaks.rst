Streaks Endpoint
================

The ``streaks`` endpoint provides access to streaks-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **2 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

getStreaks()
^^^^^^^^^^^^

**Summary:** View streaks

**Path:** ``/v1/streaks``

**Query Parameters:**

- ``streakOrg`` (*string*, *optional*): streakOrg
- ``streakStat`` (*array*, *optional*): streakStats
- ``streakSpan`` (*string*, *optional*): streakSpan
- ``streakLevel`` (*string*, *optional*): streakLevel
- ``streakThreshold`` (*integer*, *optional*): streakThreshold
- ... and 9 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View streaks
   response = api.Streaks.getStreaks(streakOrg="value", streakStat="value", streakSpan="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


highLowStats()
^^^^^^^^^^^^^^

**Summary:** View streaks parameter options

**Path:** ``/v1/streaks/types``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View streaks parameter options
   response = api.Streaks.highLowStats()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``streaks`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Streaks.get_method_names()
   print(methods)

   # Get method details
   method = api.Streaks.get_method('getStreaks')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Streaks.describe_method('getStreaks')
   print(description)
