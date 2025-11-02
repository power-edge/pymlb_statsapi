Milestones Endpoint
===================

The ``milestones`` endpoint provides access to milestones-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **6 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

achievementStatuses()
^^^^^^^^^^^^^^^^^^^^^

**Summary:** View available achievementStatus options

**Path:** ``/v1/achievementStatuses``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View available achievementStatus options
   response = api.Milestones.achievementStatuses()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


milestoneDurations()
^^^^^^^^^^^^^^^^^^^^

**Summary:** View available milestoneDurations options

**Path:** ``/v1/milestoneDurations``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View available milestoneDurations options
   response = api.Milestones.milestoneDurations()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


milestoneLookups()
^^^^^^^^^^^^^^^^^^

**Summary:** View available milestoneType options

**Path:** ``/v1/milestoneLookups``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View available milestoneType options
   response = api.Milestones.milestoneLookups()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


milestoneStatistics()
^^^^^^^^^^^^^^^^^^^^^

**Summary:** View available milestone statistics options

**Path:** ``/v1/milestoneStatistics``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View available milestone statistics options
   response = api.Milestones.milestoneStatistics()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


milestoneTypes()
^^^^^^^^^^^^^^^^

**Summary:** View available milestoneType options

**Path:** ``/v1/milestoneTypes``

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View available milestoneType options
   response = api.Milestones.milestoneTypes()
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


milestones()
^^^^^^^^^^^^

**Summary:** View pending and achieved milestones.

**Path:** ``/v1/milestones``

**Query Parameters:**

- ``orgType`` (*string*, *optional*): Organization level. Format: T(Team), L(League), S(Sport)
- ``achievementStatuses`` (*array*, *optional*): Comma delimited list of milestone achievement types
- ``milestoneTypes`` (*array*, *optional*): Comma delimited list of milestone types
- ``isLastAchievement`` (*boolean*, *optional*): Filters out milestones that have already been surpassed.
- ``milestoneStatistics`` (*array*, *optional*): Comma delimited list of milestone statistics
- ... and 9 more parameters

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View pending and achieved milestones.
   response = api.Milestones.milestones(orgType="value", achievementStatuses="value", milestoneTypes="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``milestones`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Milestones.get_method_names()
   print(methods)

   # Get method details
   method = api.Milestones.get_method('achievementStatuses')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Milestones.describe_method('achievementStatuses')
   print(description)
