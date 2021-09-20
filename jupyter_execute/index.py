#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


from msdss_base_api.core import API
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


# In[3]:


from msdss_base_api.core import API
app = API()

@app.add("GET", "/")
def hello_world():
    return "hello world!"


# In[4]:


from msdss_base_api.core import API
app = API()

def hello_world():
    return "hello world!"
app.add_route("GET", "/", hello_world)


# In[5]:


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


# In[6]:


from msdss_base_api.core import API
app = API()

def hello_world():
    return "hello world!"
app.add_route("GET", "/", hello_world)

# Run the app with app.start()
# API is hosted at http://localhost:8000
# app.start()

