# temp_ui/temp_ui.py
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from database.database import SessionLocal
from models import models
from typing import List, Tuple
from sqlalchemy.orm import joinedload
import asyncio
import json
import time

ui = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="temp_ui/templates")

# Bluetooth simulation variables
python_connection_active = False
python_weight_data = 0.0


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


@ui.get("/climber/{climber_id}/workouts", response_class=HTMLResponse)
async def climber_workouts(request: Request, climber_id: int):
    db = SessionLocal()

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


async def bluetooth_simulation_data_stream():
    global python_connection_active
    global python_weight_data
    try:
        while python_connection_active:
            python_weight_data += (0.5 - (time.time() % 1)) / 2
            if python_weight_data < 0:
                python_weight_data = 0.0
            if python_weight_data > 100:
                python_weight_data = 100
            data = {"weight": python_weight_data}
            yield json.dumps(data) + "\n"
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("Bluetooth simulation cancelled")
        python_connection_active = False
    print("Bluetooth simulation ended")


@ui.get("/start_bluetooth_python")
async def start_bluetooth_python():
    global python_connection_active
    if not python_connection_active:
        python_connection_active = True
        return StreamingResponse(bluetooth_simulation_data_stream(), media_type="text/event-stream")
    else:
        raise HTTPException(status_code=409, detail="Bluetooth connection already active")


@ui.post("/stop_bluetooth_python")
async def stop_bluetooth_python():
    global python_connection_active
    if python_connection_active:
        python_connection_active = False
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=409, detail="Bluetooth connection not active")
