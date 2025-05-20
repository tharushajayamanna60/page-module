from fastapi import FastAPI
from page import router as page_router

app = FastAPI()

app.include_router(page_router)
