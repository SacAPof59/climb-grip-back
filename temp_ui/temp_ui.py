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
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello from Jinja2!"})


@ui.get("/climbers", response_class=HTMLResponse)
async def list_climbers(request: Request):
    db = SessionLocal()
    climbers: List[models.Climber] = db.query(models.Climber).all()
    climber_models: List[models.ClimberBase] = [
        models.ClimberBase.model_validate(climber) for climber in climbers
    ]

    return templates.TemplateResponse("climbers.html", {"request": request, "climbers": climber_models})


# Create dummy files for templates and static files
# Ensure the directories exist
if not os.path.exists("temp_ui/templates"):
    os.makedirs("temp_ui/templates")
if not os.path.exists("temp_ui/static"):
    os.makedirs("temp_ui/static")

# Create a basic index.html
with open("temp_ui/templates/index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Climb Grip Back</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>{{ message }}</h1>
    <p>This is the main page.</p>
    <a href="/climbers">See Climbers</a>
</body>
</html>
""")

# Create basic climbers.html
with open("temp_ui/templates/climbers.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Climbers List</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <h1>Climbers</h1>
    <ul>
        {% for climber in climbers %}
            <li>{{ climber.first_name }} {{ climber.last_name }} - Age: {{ climber.age }}</li>
        {% endfor %}
    </ul>
    <a href="/">Go back to main</a>
</body>
</html>
""")

# Create basic styles.css
with open("temp_ui/static/styles.css", "w") as f:
    f.write("""
body {
  font-family: sans-serif;
}
  """)