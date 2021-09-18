msdss-base-api
==============

* `Github <https://www.github.com/rrwen/msdss-base-api>`_
* `License <https://github.com/rrwen/msdss-base-api/blob/master/LICENSE>`_

Base API for the Modular Spatial Decision Support Systems (MSDSS) framework.

Install
-------

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss-base-api`` via pip or through a conda environment

.. code::

   conda create -n msdss-base-api python=3.7
   conda activate msdss-base-api
   pip install msdss-base-api

Quick Start
-----------

After installing the package, use in Python:

.. code:: python

   from msdss_base_api import API
   app = API()

   # Add via function
   def hello_world():
      return "hello world!"
   app.add_route("GET", "/", hello_world)

   # Add via decorator
   @app.add("GET", "/two")
   def hello_world2():
      return "hello world 2!"

   # Run the app
   # Visit http://localhost:8000 on your browser
   app.start()

How it Works
------------

The base API wraps around `FastAPI <https://fastapi.tiangolo.com/>`_ to define routes and logic, while `Uvicorn <https://www.uvicorn.org/>`_ is used to serve programmed APIs.

.. digraph:: methods

   rankdir=LR;
   api[label="FastAPI" URL="https://fastapi.tiangolo.com/"];
   server[label="Uvicorn" URL="https://www.uvicorn.org/"];

   subgraph cluster {
      api -> server;
      label="msdss-base-api";
   }

Contact
-------

Richard Wen <rrwen.dev@gmail.com>

.. toctree:: 
   :hidden:

   self
   reference