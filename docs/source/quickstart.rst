Quick Start
===========

After installing, use in Python:

.. jupyter-execute::

   from msdss_base_api import API
   app = API()

   # Add GET route
   def hello_world():
      app.logger.info('/ accessed!')
      return "hello world!"
   app.add_route("GET", "/", hello_world)

   # Handle startup event
   def before_startup():
      print("This is run before startup.")
   app.add_event("startup", before_startup)

   # Handle shutdown event
   def during_shutdown():
      print("This is run during shutdown.")
   app.add_event("shutdown", during_shutdown)

   # Run the app with app.start()
   # API is hosted at http://localhost:8000
   # app.start()
