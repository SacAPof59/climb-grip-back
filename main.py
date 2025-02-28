# main.py
from fastapi import FastAPI
import crud
import database
from database import SessionLocal, Base, engine
from models import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/test/climber/create-test")
def create_test_climber():
    crud.create_climber(
        db=SessionLocal(),
        climber=models.Climber(
            first_name="Test",
            last_name="Climber",
            age=30,
            gender="M",
            height=180,
            span=180,
            route_grade="7a",
            boulder_grade="7a"
        )
    )

    return {"message": "Test climber created"}

@app.get("/test/load-exemple-data")
def load_example_data():
    database.extract_example_data_to_db()