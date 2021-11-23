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
    routers : list(dict)
        List of dictionaries, where each dictionary consists of:

        * ``router`` (:class:`fastapi:fastapi.routing.APIRouter`): FastAPI router object from calling :meth:`msdss_base_api.core.add_router`
        * ``args`` (tuple): positional arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_router`
        * ``kwargs`` (dict): keyword arguments passed to the FastAPI router from calling :meth:`msdss_base_api.core.add_router`

        The ``router`` and ``*args, **kwargs`` can be used to reproduce the added router to another app.

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
        @app.add("GET", "/two")
        def hello_world2():
            app.logger.info('/two accessed!')
            return "hello world 2!"

        # Run the app with app.start()
        # API is hosted at http://localhost:8000
        # app.start()
    """
    def __init__(self, api=FastAPI(title='MSDSS Base API', version='0.0.5'), logger=logging.getLogger('uvicorn.error')):
        self.api = api
        self.logger = logger
        self.routers = []

    def add(self, method, path, *args, **kwargs):
        """
        Decorator function for adding routes.

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

            @app.add("GET", "/")
            def hello_world():
                return "hello world!"
        """
        def add_decorator(func):
            self.add_route(method=method, path=path, func=func, *args, **kwargs)
        return add_decorator

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
            app = API()

            def hello_world():
                return "hello world!"
            app.add_route("GET", "/", hello_world)
        """
        self.api.add_api_route(methods=[method], path=path, endpoint=func, *args, **kwargs)

    def add_router(self, router, *args, **kwargs):
        """
        Add a router to the API.

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

    def add_routes(self, routes):
        """
        Add multiple routes using a dict to the API.

        Parameters
        ----------
        routes : list of dict
            A list of dictionaries containing routes with the same parameter names as :meth:`core.API.add_route`.

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
            
            def hello_world2():
                return "hello world 2!"

            routes = [
                {"method": "GET", "path": "/", "func": hello_world},
                {"method": "GET", "path": "/two", "func": hello_world2},
            ]

            app.add_routes(routes)
        """
        for r in routes:
            self.add_route(**r)

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

    def on(self, event, *args, **kwargs):
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

            @app.on("startup")
            def before_startup():
                print("This is run before startup.")
            
            @app.on("shutdown")
            def during_shutdown():
                print("This is run during shutdown.")

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        def on_decorator(func):
            self.on_event(event=event, func=func, *args, **kwargs)
        return on_decorator
    
    def on_event(self, event, func, *args, **kwargs):
        """
        Handles API events using a custom function.

        Parameters
        ----------
        event : str
            The event to handle. Currently supports ``startup`` (before starting) and ``shutdown`` (during shutdown).
        func : function
            Function to execute when the event occurs.
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

            def before_startup():
                print("This is run before startup.")
            app.on_event("startup", before_startup)

            def during_shutdown():
                print("This is run during shutdown.")
            app.on_event("shutdown", during_shutdown)

            # Run the app with app.start()
            # API is hosted at http://localhost:8000
            # app.start()
        """
        self.api.add_event_handler(event_type=event, func=func, *args, **kwargs)

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