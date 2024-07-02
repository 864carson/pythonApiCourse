from fastapi import FastAPI
from app import database
from app.routers import todids, users
from .database import engine

# Create any tables that don't exist
database.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todids.router)
app.include_router(users.router)
