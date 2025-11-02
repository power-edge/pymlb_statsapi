PyMLB StatsAPI Documentation
============================

A clean, Pythonic wrapper for MLB Stats API endpoints with automatic schema-driven parameter validation.

.. image:: https://github.com/power-edge/pymlb_statsapi/actions/workflows/test.yml/badge.svg
   :target: https://github.com/power-edge/pymlb_statsapi/actions/workflows/test.yml
   :alt: Tests

.. image:: https://codecov.io/gh/power-edge/pymlb_statsapi/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/power-edge/pymlb_statsapi
   :alt: codecov

.. image:: https://img.shields.io/pypi/v/pymlb-statsapi
   :target: https://pypi.org/project/pymlb-statsapi/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/pymlb-statsapi
   :target: https://pypi.org/project/pymlb-statsapi/
   :alt: Python

.. image:: https://img.shields.io/github/license/power-edge/pymlb_statsapi
   :target: https://github.com/power-edge/pymlb_statsapi/blob/main/LICENSE
   :alt: License

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # With pip
   pip install pymlb-statsapi

   # With uv (recommended)
   uv add pymlb-statsapi

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from pymlb_statsapi import api

   # Get schedule (clean parameter passing!)
   response = api.Schedule.schedule(sportId=1, date="2025-06-01")
   data = response.json()

   # Get live game data
   response = api.Game.liveGameV1(game_pk="747175", timecode="20241027_000000")
   data = response.json()

   # Save response to file
   result = response.gzip(prefix="mlb-data")

Key Features
~~~~~~~~~~~~

* **🎯 Clean API**: Parameters are intelligently routed to path or query params based on the schema configuration
* **📋 Schema-driven**: All endpoints and methods generated from JSON schemas (sourced from https://beta-statsapi.mlb.com/docs/)
* **✅ Type-safe**: Automatic parameter validation from API schemas
* **🔄 Dynamic**: Zero hardcoded models - updates via schema changes only
* **🧪 Well-tested**: Comprehensive unit tests with pytest and BDD test suite with stub capture/replay

🔍 Explore the API
~~~~~~~~~~~~~~~~~~

The **Schema Reference** is the heart of this library - browse 21 MLB Stats API endpoints with:

* Detailed parameter documentation for every method
* Working Python code examples
* Schema introspection capabilities
* Clear marking of functional vs non-functional endpoints

➡️ **Start here:** :doc:`schemas/index`

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: 📚 Schema Reference (Start Here!)

   schemas/index

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   usage
   testing
   contributing

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/factory
   api/registry
   api/endpoints

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   architecture
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
