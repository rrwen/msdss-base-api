Usage
=====

Decorators
----------

Use in Python via decorators:

.. jupyter-execute::

   from msdss_base_api import API
   app = API()

   # Add GET route
   @app.route("GET", "/two")
   def hello_world2():
      app.logger.info('/two accessed!')
      return "hello world 2!"

   # Handle startup event
   @app.event("startup")
   def before_startup2():
      print("This is run before startup.")

   # Handle shutdown event
   @app.event("shutdown")
   def during_shutdown2():
      print("This is run during shutdown.")

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

Routers
-------

Routers can be created and added:

.. jupyter-execute::

   from msdss_base_api.core import API
   app = API()

   # Add GET route
   @app.route("GET", "/two")
   def hello_world2():
      app.logger.info('/two accessed!')
      return "hello world 2!"

   # Create the router
   router = app.create_router(
         prefix='/helloworld',
         tags=['helloworld']
   )

   # Add a route
   @router.get('/start')
   def hello_world():
         return "hello world!"

   # Add router to app
   app.add_router(router)

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

Combining App Routes, Routers, and Events
-----------------------------------------

Routes, routers, and events from other apps can be combined in a single app:

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
    async def startup2():
        print("startup 2!")

    @app3.event("shutdown")
    def shutdown():
        print("shutdown!")

    # Combine apps together into app1
    app1.add_apps(app2, app3)

    # Check main app event arguments
    print('app1 combined events:\n')
    pprint(app1.events)
    print('\napp1 combined routes:\n')
    pprint(app1.routes)
    print('\napp1 combined routers:\n')
    pprint(app1.routers)

    # Run the app with app1.start()
    # Try the API at http://localhost:8000/docs
    # app1.start()