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

   # Add route via function
   def hello_world():
      return "hello world!"
   app.add_route("GET", "/", hello_world)

   # Add route via decorator
   @app.add("GET", "/two")
   def hello_world2():
      return "hello world 2!"

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

How it Works
============

The base API wraps around `FastAPI <https://fastapi.tiangolo.com/>`_ to define routes and logic, while `Uvicorn <https://www.uvicorn.org/>`_ is used to serve the APIs.

First a ``FastAPI()`` object is created, and routes are added with `.add_api_route() <https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L479>`_. Then ``uvicorn`` is used to run the app with `.run() <https://www.uvicorn.org/deployment/#running-programmatically>`_.

>>> from fastapi import FastAPI
>>> import uvicorn
>>> app = FastAPI()
>>> def helloworld(): return "hello world!"
>>> app.add_api_route(methods=["GET"], path="/", endpoint=helloworld)
>>> uvicorn.run(app)

.. digraph:: methods

   rankdir=TB;
   api[label="FastAPI" URL="https://fastapi.tiangolo.com/" style=filled];
   apimeth1[label=".add_api_route()" shape=rect style=rounded URL="https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L479"];
   server[label="Uvicorn" URL="https://www.uvicorn.org/" style=filled];
   servermeth1[label=".run()" shape=rect style=rounded URL="https://www.uvicorn.org/deployment/#running-programmatically"];

   subgraph cluster {
      label=< <B>msdss-base-api</B> >;
      style=rounded;
      {rank=min; api -> server;}
      apimeth1 -> api[arrowhead=none];
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