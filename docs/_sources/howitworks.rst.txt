How it Works
============

Adding Routes, Routers, and Events
----------------------------------

The :class:`msdss_base_api.core.API` wraps around `FastAPI <https://fastapi.tiangolo.com/>`_ to define routes and logic, while `Uvicorn <https://www.uvicorn.org/>`_ is used to serve the APIs `programmatically <https://www.uvicorn.org/deployment/#running-programmatically>`_.

First a ``FastAPI()`` object is created, and routes/routers are added with `.add_api_route() <https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L479>`_ / `.include_router() <https://github.com/tiangolo/fastapi/blob/bee35f5ae1fc58e7ab125427ad4287210e99d8b3/fastapi/routing.py#L632>`_, while API events are handled with `.add_event_handler() <https://github.com/encode/starlette/blob/6c556f6c5e4aa70173a84f6e6854390241231021/starlette/routing.py#L749>`_.
Then ``uvicorn`` is used to run the app with `.run() <https://www.uvicorn.org/deployment/#running-programmatically>`_.
These form the basis of adding routes, routers, and events.

.. digraph:: methods1

   rankdir=TB;

   api[label="FastAPI" URL="https://fastapi.tiangolo.com/" style=filled];
   apiroutemeth[label=".add_api_route()" shape=rect style=rounded];
   eventhandlermeth[label=".add_event_handler()" shape=rect style=rounded];
   routermeth[label=".add_event_handler()" shape=rect style=rounded];
   
   server[label="Uvicorn" URL="https://www.uvicorn.org/" style=filled];
   run[label=".run()" shape=rect style=rounded];
   start[label=".start()" shape=rect style=rounded];

   addevent[label=".add_event()" shape=rect style=rounded];
   addroute[label=".add_route()" shape=rect style=rounded];
   addrouter[label=".add_router()" shape=rect style=rounded];

   subgraph cluster {
      label=< <B>msdss-base-api.core.API (add_route/router/event)</B> >;
      style=rounded;
      {rank=min; api -> server;}

      apiroutemeth -> api[arrowhead=none];
      routermeth -> api[arrowhead=none];
      eventhandlermeth -> api[arrowhead=none];
      run -> server[arrowhead=none];

      apiroutemeth -> addroute;
      routermeth -> addrouter;
      eventhandlermeth -> addevent;
      run -> start;
   }

For more information on adding routes, routers, and events, see:

* :meth:`msdss_base_api.core.API.add_route`
* :meth:`msdss_base_api.core.API.add_router`
* :meth:`msdss_base_api.core.API.add_event`

Combining Routes, Routers, and Events Across Apps
-------------------------------------------------

When adding routes, routers, and events, the arguments are tracked in attributes ``routes``, ``routers``, and ``events``, which are then
used to combine routes, routers, and events from other app instances.

.. digraph:: methods2

   rankdir=TB;

   addevent[label=".add_event()" shape=rect style=rounded];
   addroute[label=".add_route()" shape=rect style=rounded];
   addrouter[label=".add_router()" shape=rect style=rounded];
   addapp[label=".add_apps()" shape=rect style=rounded];

   appevents[label=".add_app_events()" shape=rect style=rounded];
   approutes[label=".add_app_routes()" shape=rect style=rounded];
   approuters[label=".add_app_routers()" shape=rect style=rounded];

   eventattr[label=".events" shape=plain style=rounded];
   routeattr[label=".routes" shape=plain style=rounded];
   routerattr[label=".routers" shape=plain style=rounded];

   subgraph cluster {
      label=< <B>msdss-base-api.core.API (add_app_events/routes/routers)</B> >;
      style=rounded;

      addevent -> eventattr -> appevents -> addapp;
      addroute -> routeattr -> approutes -> addapp;
      addrouter -> routerattr -> approuters -> addapp;
   }

For more information on combining app routes, routers, and events, see:

* :meth:`msdss_base_api.core.API.add_apps`
* :meth:`msdss_base_api.core.API.add_app_events`
* :meth:`msdss_base_api.core.API.add_app_routes`
* :meth:`msdss_base_api.core.API.add_app_routers`