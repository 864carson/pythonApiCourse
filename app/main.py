from fastapi import FastAPI
from app import database
from app.routers import auth, health, todids, users
from .database import engine

# Create any tables that don't exist
database.Base.metadata.create_all(bind=engine)

# Create the API and wire up the routers (think controllers)
app = FastAPI()
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(todids.router)
app.include_router(users.router)


# import os
# print(os.environ)
# print(os.getenv("Path"))
