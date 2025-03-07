# temp_ui/temp_ui.py
from fastapi import FastAPI, Request, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database.database import SessionLocal, get_db
from models import models
from typing import List, Tuple
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import func
from datetime import datetime

ui = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="temp_ui/templates")


# Helper functions
def get_or_create_basic_workout_type(db: Session) -> models.WorkoutTypeEntity:
    """Retrieve or create the basic workout type."""
    basic_workout_type = db.query(models.WorkoutTypeEntity).filter_by(name="basic").first()
    if not basic_workout_type:
        basic_workout_type = models.WorkoutTypeEntity(
            name="basic",
            description="Basic workout type",
            sets_number=1,
            set_pause=0,
            repetitions=1,
            repetition_active=0,
            repetition_pause=0,
        )
        db.add(basic_workout_type)
        db.commit()
        db.refresh(basic_workout_type)
    return basic_workout_type


# Web routes (using Jinja2)
@ui.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello SacAPof59!"})


@ui.get("/climbers", response_class=HTMLResponse)
async def list_climbers(request: Request):
    db: Session = SessionLocal()
    climbers: List[models.ClimberEntity] = db.query(models.ClimberEntity).all()
    climber_models: List[models.ClimberBase] = [
        models.ClimberBase.model_validate(climber) for climber in climbers
    ]

    return templates.TemplateResponse("climbers.html", {"request": request, "climbers": climber_models})


@ui.post("/climber/{climber_id}/start_workout")
async def start_workout(request: Request, climber_id: int, db: Session = Depends(get_db)):
    """Start a new workout for a specific climber."""
    climber = db.query(models.ClimberEntity).filter(models.ClimberEntity.id == climber_id).first()
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")

    # Ensure the "basic" workout type exists
    basic_workout_type = get_or_create_basic_workout_type(db)

    # Create a new workout
    new_workout = models.WorkoutEntity(
        workout_name=basic_workout_type.name,
        climber_id=climber_id,
        body_weight=0.0,  # Initial body weight can be set here
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return JSONResponse({"workout_id": new_workout.id, "message": f"Workout created for climber {climber_id}"},
                        status_code=201)


@ui.post("/workout/{workout_id}/add_measurement")
async def add_measurement(workout_id: int, request: Request, db: Session = Depends(get_db)):
    """Add a new measurement to a workout."""
    workout = db.query(models.WorkoutEntity).filter(models.WorkoutEntity.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    measurement_device = db.query(models.MeasurementDeviceEntity).first()
    if not measurement_device:
        raise HTTPException(status_code=404, detail="Measurement Device not found")

    data = await request.json()
    weight = data.get("weight")
    battery = data.get("battery")

    if weight is None or battery is None:
        raise HTTPException(status_code=400, detail="Weight or battery data is missing")

    current_measurement_id = (db.query(func.max(models.MeasurementEntity.id)).scalar() or 0) + 1
    new_measurement = models.MeasurementEntity(id=current_measurement_id, workout_id=workout_id,
                                               measurement_device_id=measurement_device.id, current_repetition=0,
                                               created_at=datetime.now(), updated_at=datetime.now())
    db.add(new_measurement)

    new_measured_data = models.MeasuredDataEntity(measurement_id=current_measurement_id, iteration=0, weight=weight)
    db.add(new_measured_data)
    db.commit()
    return JSONResponse({"message": "Measurement added to workout"}, status_code=201)


@ui.get("/climber/{climber_id}/workouts", response_class=HTMLResponse)
async def climber_workouts(request: Request, climber_id: int):
    db: Session = SessionLocal()

    # Get climber with a simple query
    climber = db.query(models.ClimberEntity).filter(models.ClimberEntity.id == climber_id).first()
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")

    # Create Pydantic model from the climber entity
    climber_model = models.ClimberBase.model_validate(climber)

    # Get workouts with a separate query
    workouts = db.query(models.WorkoutEntity).filter(models.WorkoutEntity.climber_id == climber_id).all()

    workout_models = []
    for workout in workouts:
        # Create a base workout model without measurements
        workout_dict = {
            "id": workout.id,
            "workout_name": workout.workout_name,
            "climber_id": workout.climber_id,
            "body_weight": workout.body_weight,
            "created_at": workout.created_at,
            "updated_at": workout.updated_at,
            "measurements": []
        }

        workout_model = models.WorkoutRead.model_validate(workout_dict)

        # Now process measurements separately to avoid recursive issues
        measurements_query = (
            db.query(models.MeasurementEntity)
            .options(joinedload(models.MeasurementEntity.measurement_device))
            .filter(models.MeasurementEntity.workout_id == workout.id)
        )

        for measurement in measurements_query:
            # Create a simple measurement response object
            measurement_dict = {
                "id": measurement.id,
                "workout_id": measurement.workout_id,
                "measurement_device_id": measurement.measurement_device_id,
                "current_repetition": measurement.current_repetition,
                "created_at": measurement.created_at,
                "updated_at": measurement.updated_at,
                "measurement_device": {
                    "id": measurement.measurement_device.id,
                    "sample_rate_hz": measurement.measurement_device.sample_rate_hz
                } if measurement.measurement_device else None,
                "measured_data_for_graph": [],  # Add this line
            }

            measurement_model = models.MeasurementResponse.model_validate(measurement_dict)

            # Get measured data with a separate query to avoid recursive issues
            if measurement.measurement_device:
                sample_rate_hz = measurement.measurement_device.sample_rate_hz

                # Get measured data directly with a simple query
                measured_data = db.query(models.MeasuredDataEntity).filter(
                    models.MeasuredDataEntity.measurement_id == measurement.id
                ).all()

                for data in measured_data:
                    time = (data.iteration / sample_rate_hz)
                    weight = data.weight
                    measurement_model.measured_data_for_graph.append((time, weight))

            # Add to workout measurements
            workout_model.measurements.append(measurement_model)

        workout_models.append(workout_model)

        # Close the session
        db.close()

    return templates.TemplateResponse(
        "climber_workouts.html",
        {"request": request, "climber": climber_model, "workouts": workout_models},
    )


@ui.get("/bluetooth_test", response_class=HTMLResponse)
async def bluetooth_test_page(request: Request):
    return templates.TemplateResponse("bluetooth_test.html", {"request": request})
