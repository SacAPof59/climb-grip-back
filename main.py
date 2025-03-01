# main.py
import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from webapi import webapi
from temp_ui import temp_ui
from database.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Mount static files directory
if os.path.exists("temp_ui/static"):
    app.mount("/static", StaticFiles(directory="temp_ui/static"), name="static")
app.mount("/api/v1", webapi.api_v1)
app.mount("/", temp_ui.ui)