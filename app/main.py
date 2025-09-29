from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db, Base, engine
from app import schemas
from app.models import models
from app.routers import routes


logging.basicConfig(level=logging.INFO)


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(routes.router)