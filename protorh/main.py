import uvicorn
from fastapi import FastAPI
import sys

# routes imports
from routes import events, requestRH, test, users, connect, upload

# run on diffenrent port with args if not working
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 4242

description = """
Our Amazing API helps you do awesome stuff. 🚀

## Events

You can:

* Get **all events**
* Get **event by id**
* **Create** an event
* **Update** an event
* **Delete** an event

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Our Amazing API",
    description=description,
    summary="This is our API project in Python3",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
)

# routes
app.include_router(events.router, prefix="/api")
app.include_router(requestRH.router, prefix="/api")
app.include_router(test.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(connect.router, prefix="/api")
app.include_router(upload.router, prefix="/api")


# Endpoint : /
# Type : GET
# return API is working
@app.get("/")
async def root():
    return "REST API is working yey"


# Endpoint : /api/hello
# Type : GET
# this endpoint return à json string containing "Hello world !"
@app.get("/api/hello")
async def hello():
    return {"message": "hello world !"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
