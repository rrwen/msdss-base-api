msdss-base-api
==============

Base API for the Modular Spatial Decision Support Systems (MSDSS) framework.


* `Github <https://www.github.com/rrwen/msdss-base-api>`_
* `License <https://github.com/rrwen/msdss-base-api/blob/master/LICENSE>`_

Install
=======

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss-base-api`` via pip or through a conda environment

.. code::

   conda create -n msdss-base-api python=3.7
   conda activate msdss-base-api
   pip install msdss-base-api

Quick Start
===========

After installing the package, use in Python:

.. jupyter-execute::

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

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

How it Works
============

The base API wraps around `FastAPI <https://fastapi.tiangolo.com/>`_ to define routes and logic, while `Uvicorn <https://www.uvicorn.org/>`_ is used to serve the APIs.

.. digraph:: methods

   rankdir=LR;
   api[label="FastAPI" URL="https://fastapi.tiangolo.com/"];
   server[label="Uvicorn" URL="https://www.uvicorn.org/"];

   subgraph cluster {
      api -> server;
      label="msdss-base-api";
   }

API Reference
=============

.. autoclass:: msdss_base_api.core.API
    :members:

.. toctree:: 
   :maxdepth: 2
   :hidden:

   index

Contact
=======

Richard Wen <rrwen.dev@gmail.com>