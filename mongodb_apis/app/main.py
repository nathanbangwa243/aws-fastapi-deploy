# -*- coding: utf-8 -*-
    
from fastapi import FastAPI
from mangum import Mangum

import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

print("AWS_ACCESS_KEY_ID : ", AWS_ACCESS_KEY_ID)
print("GEMINI_MODEL_NAME : ", AWS_SECRET_ACCESS_KEY)

env_str = f"AWS_ACCESS_KEY_ID : {AWS_ACCESS_KEY_ID} - AWS_SECRET_ACCESS_KEY : {AWS_SECRET_ACCESS_KEY}"

# if __name__ == "app.main":
#     # for tests purpose
#     from .routers import *
# else:
#     from routers import *
app = FastAPI()

@app.get("/")
async def read_main():
    return {"message": "Welcome to your new MongoDB API", "env": env_str}

# ADD ROUTERS

# app.include_router(categories.router)


# Add Mangum Handler

handler = Mangum(app)
