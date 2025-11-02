Job Endpoint
============

The ``job`` endpoint provides access to job-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **4 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

datacasters()
^^^^^^^^^^^^^

**Summary:** Get jobs by type

**Path:** ``/v1/jobs/datacasters``

**Query Parameters:**

- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get jobs by type
   response = api.Job.datacasters(sportId=1, date="2024-07-04", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


getJobsByType()
^^^^^^^^^^^^^^^

**Summary:** Get jobs by type

**Path:** ``/v1/jobs``

**Query Parameters:**

- ``jobType`` (*string*, **required**): Job Type Identifier (ie. UMPR, etc..)
- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get jobs by type
   response = api.Job.getJobsByType(jobType="value", sportId=1, date="2024-07-04")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


officialScorers()
^^^^^^^^^^^^^^^^^

**Summary:** Get jobs by type

**Path:** ``/v1/jobs/officialScorers``

**Query Parameters:**

- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get jobs by type
   response = api.Job.officialScorers(sportId=1, date="2024-07-04", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


umpires()
^^^^^^^^^

**Summary:** Get jobs by type

**Path:** ``/v1/jobs/umpires``

**Query Parameters:**

- ``sportId`` (*integer*, *optional*): Top level organization of a sport
- ``date`` (*LocalDate*, *optional*): Date of Game. Format: YYYY-MM-DD
- ``fields`` (*array*, *optional*): Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute
- ``season`` (*integer*, *optional*): Season of play

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # Get jobs by type
   response = api.Job.umpires(sportId=1, date="2024-07-04", fields="value")
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``job`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Job.get_method_names()
   print(methods)

   # Get method details
   method = api.Job.get_method('getJobsByType')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Job.describe_method('getJobsByType')
   print(description)
