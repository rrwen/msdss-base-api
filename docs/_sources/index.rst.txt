msdss-base-api
==============

* `Github <https://www.github.com/rrwen/msdss-base-api>`_
* `License <https://github.com/rrwen/msdss-base-api/blob/master/LICENSE>`_

Base API for the Modular Spatial Decision Support Systems (MSDSS) framework.

Install
-------

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss_base_api`` via pip or through a conda environment

.. code::

    conda create -n msdss_base_api python=3.7
    conda activate msdss_base_api
    pip install git+https://github.com/rrwen/msdss_base_api

Quick Start
-----------

Use in Python:

.. code:: python

    from msdss_base_api import API
    app = API()

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

Richard Wen rrwen.dev@gmail.com

Contents
--------

.. toctree:: 
   :numbered:

   self