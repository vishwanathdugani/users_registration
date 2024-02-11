# main.py
import logging
from fastapi import FastAPI
from app.api.endpoints import login, users
from app.core import config
from app.db.base import Base
from app.db.sessions import engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

app = FastAPI()

app.include_router(login.router, prefix=config.settings.API_V1_STR, tags=["login"])
app.include_router(users.router, prefix=config.settings.API_V1_STR, tags=["users"])

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created")
