import json
import os
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func

from database import crud
from database.database import SessionLocal
from models import models


def extract_example_data_to_db():
    exemple_data_list = _load_exemple_data()
    db = SessionLocal()
    for exemple_data in exemple_data_list:
        _import_to_db(db, exemple_data)


def _load_exemple_data():
    data_dir = "./example_data"
    if not os.path.exists(data_dir):
        raise HTTPException(status_code=404, detail=f"Data directory '{data_dir}' not found")

    exemple_data_list = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r") as f:
                    exemple_data_list.append(json.load(f))
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail=f"File '{filename}' is not a valid json")

    return exemple_data_list


def _import_to_db(db, data):
    # Extract climber name
    filename = data.get("filename")
    personal_info = data.get("Personal", {})
    climber_first_name = personal_info.get("name", "None").split(" ")[0]
    climber_last_name = " ".join(personal_info.get("name", "None").split(" ")[1:])
    if len(climber_last_name) < 1:
        climber_last_name = "None"

    # Find the climber
    climber = db.query(models.ClimberEntity).filter_by(first_name=climber_first_name, last_name=climber_last_name).first()

    if climber is None:
        # If the climber doesn't exist, create them
        climber = models.ClimberEntity(
            first_name=climber_first_name,
            last_name=climber_last_name,
            age=personal_info.get("age", None),  # Extract from JSON or set to None
            gender=personal_info.get("gender", None),  # Extract from JSON or set to None
            height=personal_info.get("height", None),  # Extract from JSON or set to None
            span=personal_info.get("span", None),  # Extract from JSON or set to None
            route_grade=personal_info.get("routeGrade", None),  # Extract from JSON or set to None
            boulder_grade=personal_info.get("boulderGrade", None)  # Extract from JSON or set to None
        )
        climber = crud.create_climber(db=db, climber=climber)

    # Create a workout type if it doesn't exist
    measurement_info = data.get("Measurement", {})
    workout_type_name = measurement_info.get("workout", "Custom")
    workout_type = db.query(models.WorkoutTypeEntity).filter_by(name=workout_type_name).first()
    if workout_type is None:
        workout_type = models.WorkoutTypeEntity(
            name=workout_type_name,
            description=workout_type_name,  # Extract from JSON or set to a default
        )
        workout_type = crud.create_workout_type(db=db, workout_type=workout_type)
    # Create a workout associated with the climber
    workout = models.WorkoutEntity(
        workout_name=workout_type.name,
        climber_id=climber.id,
        body_weight=measurement_info.get("weight", None),  # Extract from JSON or set to None
        created_at=datetime.strptime(measurement_info.get("timestamp"), "%Y-%m-%d %H:%M:%S") if measurement_info.get(
            "timestamp") else func.now(),  # Extract from file name
        updated_at=func.now()
    )
    workout = crud.create_workout(db=db, workout=workout)

    # Create the measurement device
    measurement_device = db.query(models.MeasurementDeviceEntity).first()
    if measurement_device is None:
        measurement_device = models.MeasurementDeviceEntity(
            sample_rate_hz=10
        )
        measurement_device = crud.create_measurement_device(db=db, measurement_device=measurement_device)

    # Create a single measurement
    measurement = models.MeasurementEntity(
        workout_id=workout.id,
        measurement_device_id=measurement_device.id,
        current_repetition=1,
        created_at=datetime.strptime(measurement_info.get("timestamp"),
                                     "%Y-%m-%d %H:%M:%S") if measurement_info.get("timestamp") else func.now(),
        updated_at=func.now()
    )
    measurement = crud.create_measurement(db=db, measurement=measurement)
    # Create measured data associated with this measurement
    for i, weight in enumerate(measurement_info.get("measDataKg", [])):
        measured_data = models.MeasuredDataEntity(
            measurement_id=measurement.id,
            iteration=i + 1,
            weight=weight
        )
        crud.create_measured_data(db=db, measured_data=measured_data)