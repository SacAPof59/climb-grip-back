'''
WebAPI endpoints that will be of future usage for frontend migration to a proper Javascript frontend framework
'''
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import crud
from database.database import SessionLocal
from database.import_tool import extract_example_data_to_db
from models import models

api_v1 = FastAPI(title="Climb Grip Back API v1")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api_v1.get("/climber/{climber_id}", response_model=models.ClimberBase)
def get_climber(climber_id: int, db: Session = Depends(get_db)):
    climber = crud.get_climber(db=db, climber_id=climber_id)
    if climber is None:
        raise HTTPException(status_code=404, detail="Climber not found")
    return models.ClimberBase.model_validate(climber)


@api_v1.get("/climber", response_model=List[models.ClimberBase])
def get_all_climbers(db: Session = Depends(get_db)):
    climbers = db.query(models.ClimberEntity).all()
    if climbers is None:
        raise HTTPException(status_code=404, detail="Climbers not found")
    return [models.ClimberBase.model_validate(climber) for climber in climbers]


@api_v1.get("/test/climber/create-test")
def create_test_climber(db: Session = Depends(get_db)):
    climber = models.ClimberEntity(
        first_name="Test",
        last_name="Climber",
        age=30,
        gender="M",
        height=180,
        span=180,
        route_grade="7a",
        boulder_grade="7a",
    )
    crud.create_climber(db=db, climber=climber)

    return {"message": "Test climber created"}


@api_v1.get("/test/load-exemple-example_data")
def load_example_data(db: Session = Depends(get_db)):
    extract_example_data_to_db()
    return {"message": "exemple example_data loaded"}