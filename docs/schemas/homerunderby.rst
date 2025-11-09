Homerunderby Endpoint
=====================

The ``homerunderby`` endpoint provides access to homerunderby-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **6 functional methods** and **0 non-functional methods**.

Functional Methods
--------------------------------------------------

The following methods are fully functional and tested:

__homeRunDerbyBracket_base()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby/bracket``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.__homeRunDerbyBracket_base(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__homeRunDerbyBracket_gamePk()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby/{gamePk}/bracket``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.__homeRunDerbyBracket_gamePk(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__homeRunDerbyPool_base()
^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby/pool``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.__homeRunDerbyPool_base(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


__homeRunDerbyPool_gamePk()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby/{gamePk}/pool``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.__homeRunDerbyPool_gamePk(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


homeRunDerbyBracket()
^^^^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.homeRunDerbyBracket(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")


homeRunDerbyPool()
^^^^^^^^^^^^^^^^^^

**Summary:** View a home run derby object

**Path:** ``/v1/homeRunDerby/pool``

**Path Parameters:**

- ``gamePk`` (*integer*, **required**): Unique Primary Key Representing a Game

**Query Parameters:**

- ``fields`` (*array*, *optional*): fields

**Example:**

.. code-block:: python

   from pymlb_statsapi import api

   # View a home run derby object
   response = api.Homerunderby.homeRunDerbyPool(fields="value", gamePk=1)
   data = response.json()

   # Save to file
   result = response.gzip(prefix="mlb-data")
   print(f"Saved to: {result['path']}")



Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``homerunderby`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Homerunderby.get_method_names()
   print(methods)

   # Get method details
   method = api.Homerunderby.get_method('homeRunDerbyBracket')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Homerunderby.describe_method('homeRunDerbyBracket')
   print(description)
