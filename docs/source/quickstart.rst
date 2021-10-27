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

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()

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