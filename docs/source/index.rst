msdss-base-api
==============

Base API for the Modular Spatial Decision Support Systems (MSDSS) framework.


* `PyPi <https://pypi.org/project/msdss-base-api/>`_
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

After installing the package, use in Python via methods:

.. jupyter-execute::

   from msdss_base_api import API
   app = API()

   # Add GET route
   def hello_world():
      return "hello world!"
   app.add_route("GET", "/", hello_world)

   # Handle startup event
   def before_startup():
      print("This is run before startup.")
   app.on_event("startup", before_startup)

   # Handle shutdown event
   def during_shutdown():
      print("This is run during shutdown.")
   app.on_event("shutdown", during_shutdown)

or decorators:

.. jupyter-execute::

   from msdss_base_api import API
   app = API()

   # Add GET route
   @app.add("GET", "/two")
   def hello_world2():
      return "hello world 2!"

   # Handle startup event
   @app.on("startup")
   def before_startup2():
      print("This is run before startup.")

   # Handle shutdown event
   @app.on("shutdown")
   def during_shutdown2():
      print("This is run during shutdown.")

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

How it Works
============

The base API wraps around `FastAPI <https://fastapi.tiangolo.com/>`_ to define routes and logic, while `Uvicorn <https://www.uvicorn.org/>`_ is used to serve the APIs.

First a ``FastAPI()`` object is created, and routes are added with `.add_api_route() <https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L479>`_, while API events are handled with `add_event_handler <https://github.com/encode/starlette/blob/6c556f6c5e4aa70173a84f6e6854390241231021/starlette/routing.py#L749>`_. Then ``uvicorn`` is used to run the app with `.run() <https://www.uvicorn.org/deployment/#running-programmatically>`_.

>>> from fastapi import FastAPI
>>> import uvicorn
>>> app = FastAPI()
>>> def helloworld(): return "hello world!"
>>> app.add_api_route(methods=["GET"], path="/", endpoint=helloworld)
>>> def before_startup(): print("This is run before startup.")
>>> app.add_event_handler(event_type="startup", func=before_startup)
>>> uvicorn.run(app)

.. digraph:: methods

   rankdir=TB;
   api[label="FastAPI" URL="https://fastapi.tiangolo.com/" style=filled];
   apimeth1[label=".add_api_route()" shape=rect style=rounded URL="https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L479"];
   apimeth2[label=".add_event_handler()" shape=rect style=rounded URL="https://github.com/encode/starlette/blob/6c556f6c5e4aa70173a84f6e6854390241231021/starlette/routing.py#L749"];
   server[label="Uvicorn" URL="https://www.uvicorn.org/" style=filled];
   servermeth1[label=".run()" shape=rect style=rounded URL="https://www.uvicorn.org/deployment/#running-programmatically"];

   subgraph cluster {
      label=< <B>msdss-base-api</B> >;
      style=rounded;
      {rank=min; api -> server;}
      apimeth1 -> api[arrowhead=none];
      apimeth2 -> api[arrowhead=none];
      servermeth1 -> server[arrowhead=none];
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