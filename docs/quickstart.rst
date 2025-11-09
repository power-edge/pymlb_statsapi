Quick Start
===========

Basic Usage
-----------

.. code-block:: python

   from pymlb_statsapi import api

   # Get schedule
   response = api.Schedule.schedule(sportId=1, date="2025-06-01")
   data = response.json()

   # Get game data
   response = api.Game.liveGameV1(game_pk="747175")
   data = response.json()

For more examples, see the :doc:`usage` guide.
