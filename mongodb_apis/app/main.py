# -*- coding: utf-8 -*-
    
from fastapi import FastAPI
from mangum import Mangum

# if __name__ == "app.main":
#     # for tests purpose
#     from .routers import *
# else:
#     from routers import *
app = FastAPI()

@app.get("/")
async def read_main():
    return {"message": "Welcome to your new MongoDB API"}

# ADD ROUTERS

# app.include_router(categories.router)


# Add Mangum Handler

handler = Mangum(app)
