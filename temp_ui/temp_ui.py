# temp_ui/temp_ui.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.database import SessionLocal
from models import models
from typing import List
import os

ui = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="temp_ui/templates")

# Web routes (using Jinja2)
@ui.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello SacAPof59!"})


@ui.get("/climbers", response_class=HTMLResponse)
async def list_climbers(request: Request):
    db = SessionLocal()
    climbers: List[models.ClimberEntity] = db.query(models.ClimberEntity).all()
    climber_models: List[models.ClimberBase] = [
        models.ClimberBase.model_validate(climber) for climber in climbers
    ]

    return templates.TemplateResponse("climbers.html", {"request": request, "climbers": climber_models})
