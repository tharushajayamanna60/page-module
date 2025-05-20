from fastapi import FastAPI
from page import router as page_router

app = FastAPI()

app.include_router(page_router)

from models import Base
from database import engine

Base.metadata.create_all(bind=engine)
