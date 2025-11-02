Gamepace Endpoint
=================

The ``gamepace`` endpoint provides access to gamepace-related data from the MLB Stats API.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------------------------------------------------

This endpoint has **0 functional methods** and **0 non-functional methods**.


Schema Introspection
--------------------------------------------------

You can explore the full schema for the ``gamepace`` endpoint programmatically:

.. code-block:: python

   from pymlb_statsapi import api

   # List all methods
   methods = api.Gamepace.get_method_names()
   print(methods)

   # Get method details
   method = api.Gamepace.get_method('method_name')
   schema = method.get_schema()
   print(json.dumps(schema, indent=2))

   # Get detailed description
   description = api.Gamepace.describe_method('method_name')
   print(description)
