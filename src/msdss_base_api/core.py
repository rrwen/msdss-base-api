import logging
import uvicorn

from fastapi import FastAPI, APIRouter

class API:
    """
    Base class for mSDSS related APIs.

    Parameters
    ----------
    api : :class:`fastapi:fastapi.FastAPI`
        API object to use for creating routes.
    logger : :class:`logging.Logger`
        Object for logging. Instantiated with :func:`logging.getLogger`.

    Attributes
    ----------
    api : :class:`fastapi.FastAPI`
        API object passed from parameter ``api``.
    logger : :class:`logging.Logger`
        Object for logging from parameter ``logger``.
    routes : list(dict)
        List of dictionaries, where each dictionary represents arguments for adding a route:

        * ``method`` (str): request method for route
        * ``path`` (str): path for route
        * ``func`` (func): function for route
        * ``args`` (tuple): positional arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_route`
        * ``kwargs`` (dict): keyword arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_route`

        These arguments can be used to reproduce the added route to another app.

    routers : list(dict)
        List of dictionaries, where each dictionary represents arguments for adding a router:

        * ``router`` (:class:`fastapi:fastapi.routing.APIRouter`): FastAPI router object from calling :meth:`msdss_base_api.core.add_router`
        * ``args`` (tuple): positional arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_router`
        * ``kwargs`` (dict): keyword arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_router`

        These arguments can be used to reproduce the added router to another app.

    events : list(dict)
        List of dictionaries, where each dictionary represents arguments for adding an event:

        * ``event`` (str): the event type to handle
        * ``func`` (func): the function to call for the event

        These arguments can be used to reproduce the added event to another app.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_api.core import API
        app = API()

        # Add route via function
        def hello_world():
            app.logger.info('/ accessed!')
            return "hello world!"
        app.add_route("GET", "/", hello_world)

        # Add route via decorator
        @app.route("GET", "/two")
        def hello_world2():
            app.logger.info('/two accessed!')
            return "hello world 2!"

        # Run the app with app.start()
        # API is hosted at http://localhost:8000
        # app.start()
    """
    def __init__(self, api=FastAPI(title='MSDSS Base API', version='0.1.0'), logger=logging.getLogger('uvicorn.error')):
        self.api = api
        self.logger = logger
        self.routes = []
        self.routers = []
        self.events = []

    def add_apps(self, *apps, add_events=True, add_routes=True, add_routers=True):
        """
        Combines multiple apps by:
        
        * Combining app events via :meth:`msdss_base_api.core.API.add_app_events`
        * Combining app routes via :meth:`msdss_base_api.core.API.add_app_routes`
        * Combining app routers via :meth:`msdss_base_api.core.API.add_app_routers`

        Parameters
        ----------
        *apps : :class:`msdss_base_api.core.API`
            Apps to combine.
        add_events : bool
            Whether to combine events for each app or not.
        add_routes : bool
            Whether to combine routes for each app or not.
        add_routers : bool
            Whether to combine routers for each app or not.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint

            # Create apps
            app1 = API()
            app2 = API()
            app3 = API()

            # Add routes
            @app1.route('GET', '/start1')
            def hello_world1():
                return "hello world 1!"

            @app2.route('GET', '/start2')
            def hello_world2():
                return "hello world 2!"

            @app3.route('GET', '/start3')
            def hello_world3():
                return "hello world 3!"

            # Create routers
            router1 = app1.create_router(
                prefix='/helloworld1'
            )
            router2 = app2.create_router(
                prefix='/helloworld2'
            )
            router3 = app3.create_router(
                prefix='/helloworld3'
            )

            # Add router routes
            @router1.get('/start1')
            def hello_world1():
                return "hello world 1!"

            @router2.get('/start2')
            def hello_world2():
                return "hello world 2!"

            @router3.get('/start3')
            def hello_world3():
                return "hello world 3!"

            # Add routers
            app1.add_router(router1, tags=['helloworld1'])
            app2.add_router(router2, tags=['helloworld2'])
            app3.add_router(router3, tags=['helloworld3'])

            # Add events
            @app1.event("startup")
            def startup1():
                print("startup 1!")

            @app2.event("startup")
            def startup2():
                print("startup 2!")

            @app3.event("shutdown")
            def shutdown():
                print("shutdown!")

            # Combine apps together into app1
            app1.add_apps(app2, app3)

            # Check main app event arguments
            print('app1 combined events:\\n')
            pprint(app1.events)
            print('\\napp1 combined routes:\\n')
            pprint(app1.routes)
            print('\\napp1 combined routers:\\n')
            pprint(app1.routers)

            # Run the app with app1.start()
            # API is hosted at http://localhost:8000
            # app1.start()
        """
        if add_routes:
            self.add_app_routes(*apps)
        if add_routers:
            self.add_app_routers(*apps)
        if add_events:
            self.add_app_events(*apps)
    add_app = add_apps

    def add_app_events(self, *apps):
        """
        Combines event functions from several apps to the API via :meth:`msdss_base_api.core.API.add_event`.

        * Each event ``func`` will be run one after another and added based on ``event`` type
        * For example, all ``startup`` event functions from all apps will be collected into a single function and added as a single event function, which runs each function one after another
        * The result is one function for each event type

        Parameters
        ----------
        *apps : :class:`msdss_base_api.core.API`
            Apps to add events from.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint

            # Create apps
            app1 = API()
            app2 = API()
            app3 = API()

            # Add events
            @app1.event("startup")
            def startup1():
                print("startup 1!")

            @app2.event("startup")
            def startup2():
                print("startup 2!")

            @app3.event("shutdown")
            def shutdown():
                print("shutdown!")

            # Add events from other apps to main app
            app1.add_app_events(app2, app3)

            # Check main app event arguments
            print('app1 startup event combined with app2 startup event:\\n')
            pprint(app1.events[0])
            print('\\napp3 shutdown event added to app1:\\n')
            pprint(app1.events[1])

            # Run the app with app1.start()
            # API is hosted at http://localhost:8000
            # app1.start()
        """

        # (API_add_app_events_collect) Collects event functions from all apps
        event_funcs = {}
        apps = list(apps)
        apps.append(self)
        for a in apps:
            for e in a.events:
                event = e['event']
                func = e['func']
                if event not in event_funcs:
                    event_funcs[event] = []
                else:
                    event_funcs[event].append(func)
        
        # (API_add_app_events_replace) Replace event functions based on event type
        self.events = []
        for event, func_list in event_funcs.items():
            def func():
                for run in func_list:
                    run()
            self.add_event(event=event, func=func)
    add_app_event = add_app_events

    def add_app_routes(self, *apps):
        """
        Adds routes from several apps to the API via :meth:`msdss_base_api.core.API.add_route`.

        Parameters
        ----------
        *apps : :class:`msdss_base_api.core.API`
            Apps to add routes from.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint

            # Create apps
            app1 = API()
            app2 = API()
            app3 = API()

            # Add routes
            @app1.route('GET', '/start1')
            def hello_world1():
                return "hello world 1!"

            @app2.route('GET', '/start2')
            def hello_world2():
                return "hello world 2!"

            @app3.route('GET', '/start3')
            def hello_world3():
                return "hello world 3!"

            # Add routes from other apps to main app
            app1.add_app_routes(app2, app3)

            # Check main app route arguments
            print('app1 route:\\n')
            pprint(app1.routes[0])
            print('\\napp2 route added to app1:\\n')
            pprint(app1.routes[1])
            print('\\napp3 route added to app1:\\n')
            pprint(app1.routes[2])

            # Run the app with app1.start()
            # API is hosted at http://localhost:8000
            # app1.start()
        """
        for a in apps:
            for r in a.routes:
                method = r['method']
                path = r['path']
                func = r['func']
                args = r['args']
                kwargs = r['kwargs']
                self.add_route(method=method, path=path, func=func, *args, **kwargs)
    add_app_route = add_app_routes

    def add_app_routers(self, *apps):
        """
        Adds routers from several apps to the API via :meth:`msdss_base_api.core.API.add_router`.

        Parameters
        ----------
        *apps : :class:`msdss_base_api.core.API`
            Apps to add routers from.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint

            # Create apps
            app1 = API()
            app2 = API()
            app3 = API()

            # Create routers
            router1 = app1.create_router(
                prefix='/helloworld1'
            )
            router2 = app2.create_router(
                prefix='/helloworld2'
            )
            router3 = app3.create_router(
                prefix='/helloworld3'
            )

            # Add routes
            @router1.get('/start1')
            def hello_world1():
                return "hello world 1!"

            @router2.get('/start2')
            def hello_world2():
                return "hello world 2!"

            @router3.get('/start3')
            def hello_world3():
                return "hello world 3!"

            # Add routers
            app1.add_router(router1, tags=['helloworld1'])
            app2.add_router(router2, tags=['helloworld2'])
            app3.add_router(router3, tags=['helloworld3'])

            # Add routers from other apps to main app
            app1.add_app_routers(app2, app3)

            # Check main app router arguments
            print('app1 router:\\n')
            pprint(app1.routers[0])
            print('\\napp2 router added to app1:\\n')
            pprint(app1.routers[1])
            print('\\napp3 router added to app1:\\n')
            pprint(app1.routers[2])

            # Run the app with app1.start()
            # API is hosted at http://localhost:8000
            # app1.start()
        """
        for a in apps:
            for r in a.routers:
                router = r['router']
                args = r['args']
                kwargs = r['kwargs']
                self.add_router(router=router, *args, **kwargs)
    add_app_router = add_app_routers

    def add_event(self, event, func):
        """
        Handles API events using a custom function.

        Also adds the arguments passed to the attribute ``events``.

        Parameters
        ----------
        event : str
            The event to handle. Currently supports ``startup`` (before starting) and ``shutdown`` (during shutdown).
        func : function
            Function to execute when the event occurs.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint
            app = API()

            def before_startup():
                print("This is run before startup.")
            app.add_event("startup", before_startup)

            def during_shutdown():
                print("This is run during shutdown.")
            app.add_event("shutdown", during_shutdown)

            # Check router arguments
            print('startup\\n')
            pprint(app.events[0])
            print('\\nshutdown\\n')
            pprint(app.events[1])

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        arguments = locals()
        del arguments['self']
        self.events.append(arguments)
        self.api.add_event_handler(event_type=event, func=func)

    def add_route(self, method, path, func, *args, **kwargs):
        """
        Add a route to the API.

        Parameters
        ----------
        method : str
            HTTP request method (GET, POST, PUT, DELETE, etc).
        path : str
            Path (e.g. "/") of the route for the API.
        func : function
            Function to execute when route is reached.
        *args, **kwargs
            Additional arguments passed to the :meth:`fastapi:fastapi.FastAPI.add_route` method.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint
            app = API()

            # Add route
            def hello_world():
                return "hello world!"
            app.add_route("GET", "/", hello_world)

            # Check route arguments
            pprint(app.routes[0])
        """
        arguments = locals()
        del arguments['self']
        self.routes.append(arguments)
        self.api.add_api_route(methods=[method], path=path, endpoint=func, *args, **kwargs)

    def add_router(self, router, *args, **kwargs):
        """
        Add a router to the API.

        Also adds the arguments passed to the attribute ``routers``.

        Parameters
        ----------
        router : :class:`fastapi:fastapi.routing.APIRouter`
            FastAPI router object to add.
        *args, **kwargs
            Additional arguments passed to the meth:`fastapi:fastapi.FastAPI.include_router` method. See `FastAPI bigger apps <https://fastapi.tiangolo.com/tutorial/bigger-applications/>`_

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            from pprint import pprint
            app = API()

            # Create the router
            router = app.create_router(
                prefix='/helloworld'
            )

            # Add a route
            @router.get('/start')
            def hello_world():
                return "hello world!"

            # Add router to app
            app.add_router(router, tags=['helloworld'])

            # Check router arguments
            pprint(app.routers[0])

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        arguments = locals()
        del arguments['self']
        self.routers.append(arguments)
        self.api.include_router(router=router, *args, **kwargs)

    def create_router(self, *args, **kwargs):
        """
        Create a router.

        Parameters
        ----------
        *args, **kwargs
            Additional arguments passed to the class:`fastapi:fastapi.routing.APIRouter` class. See `FastAPI bigger apps <https://fastapi.tiangolo.com/tutorial/bigger-applications/>`_
        
        Return
        ------
        :class:`fastapi:fastapi.routing.APIRouter`
            A router object used for organizing larger applications and for modularity.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            app = API()

            # Create the router
            router = app.create_router(
                prefix='/helloworld',
                tags=['helloworld']
            )
        """
        out = APIRouter(*args, **kwargs)
        return out

    def event(self, event, *args, **kwargs):
        """
        Decorator function for handling events.

        Parameters
        ----------
        event : str
            The event to handle. Currently supports ``startup`` (before starting) and ``shutdown`` (during shutdown).
        *args, **kwargs
            Additional arguments passed to the :meth:`fastapi:fastapi.FastAPI.add_event_handler` method.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            app = API()

            @app.event("startup")
            def before_startup():
                print("This is run before startup.")
            
            @app.event("shutdown")
            def during_shutdown():
                print("This is run during shutdown.")

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        def event_decorator(func):
            self.add_event(event=event, func=func, *args, **kwargs)
        return event_decorator

    def route(self, method, path, *args, **kwargs):
        """
        Decorator function for adding routes.

        Also adds the arguments passed to the attribute ``routes``.

        Parameters
        ----------
        method : str
            HTTP request method (GET, POST, PUT, DELETE, etc).
        path : str
            Path (e.g. "/") of the route for the API.
        *args, **kwargs
            Additional arguments passed to the :meth:`fastapi:fastapi.FastAPI.add_route` method.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            app = API()

            @app.route("GET", "/")
            def hello_world():
                return "hello world!"
        """
        def route_decorator(func):
            self.add_route(method=method, path=path, func=func, *args, **kwargs)
        return route_decorator

    def start(self, host="127.0.0.1", port=8000, log_level="info", *args, **kwargs):
        """
        Starts a server to host the API.

        Parameters
        ----------
        host : str
            Host address for the server.
        port : int
            Port number of the host.
        log_level : str
            Level of verbose messages to display and log.
        *args, **kwargs
            Additional arguments passed to the ``uvicorn.run`` method.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_api.core import API
            app = API()

            def hello_world():
                return "hello world!"
            app.add_route("GET", "/", hello_world)

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        uvicorn.run(self.api, host=host, port=port, log_level="info", *args, **kwargs)