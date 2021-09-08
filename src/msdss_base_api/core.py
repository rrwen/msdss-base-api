import uvicorn

from fastapi import FastAPI

class API:
    """
    Base class for mSDSS related APIs.

    Parameters
    ----------
    api : :class:`fastapi:fastapi.FastAPI`
        API object to use for creating routes.

    Attributes
    ----------
    api : :class:`fastapi:fastapi.FastAPI`
        API object passed from parameter ``api``.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    >>> from msdss_base_api import API
    >>> api = API()
    >>> def hello_world: return "hello world!"
    >>> api.add_route("GET", "/", hello_world)
    >>> api.start()

    """
    def __init__(self, api=FastAPI()):
        self.app = api

    def add(self, method, path, *args, **kwargs):
        def add_decorator(func):
            self.add_route(method=method, path=path, func=func, *args, **kwargs)
        return add_decorator

    def add_route(self, method, path, func, *args, **kwargs):
        self.app.add_api_route(methods=[method], path=path, endpoint=func, *args, **kwargs)

    def add_routes(self, routes):
        for r in routes:
            self.add_route(**r)

    def start(self, host="127.0.0.1", port=8000, log_level="info", *args, **kwargs):
        uvicorn.run(self.app, host=host, port=port, log_level="info", *args, **kwargs)