from sqlalchemy.orm import Session
from models.models import Climber, MeasurementDevice, WorkoutType, Workout, Measurement, MeasuredData, \
    CriticalForceWorkout, MaxIsoStrengthWorkout


def create_climber(db: Session, climber: Climber):
    db.add(climber)
    db.commit()
    db.refresh(climber)
    return climber

def create_measurement_device(db: Session, measurement_device: MeasurementDevice):
    db.add(measurement_device)
    db.commit()
    db.refresh(measurement_device)
    return measurement_device

def create_workout_type(db: Session, workout_type: WorkoutType):
    db.add(workout_type)
    db.commit()
    db.refresh(workout_type)
    return workout_type


def create_workout(db: Session, workout: Workout):
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def create_measurement(db: Session, measurement: Measurement):
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


def create_measured_data(db: Session, measured_data: MeasuredData):
    db.add(measured_data)
    db.commit()
    db.refresh(measured_data)
    return measured_data


def create_critical_force_workout(db: Session, critical_force_workout: CriticalForceWorkout):
    db.add(critical_force_workout)
    db.commit()
    db.refresh(critical_force_workout)
    return critical_force_workout


def create_max_iso_strength_workout(db: Session, max_iso_strength_workout: MaxIsoStrengthWorkout):
    db.add(max_iso_strength_workout)
    db.commit()
    db.refresh(max_iso_strength_workout)
    return max_iso_strength_workout