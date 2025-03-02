from sqlalchemy.orm import Session
from models.models import (
    ClimberEntity,
    MeasurementDeviceEntity,
    WorkoutTypeEntity,
    WorkoutEntity,
    MeasurementEntity,
    MeasuredDataEntity,
    CriticalForceWorkoutEntity,
    MaxIsoStrengthWorkoutEntity,
)


# Climber CRUD Operations
def get_climber(db: Session, climber_id: int):
    return db.query(ClimberEntity).filter(ClimberEntity.id == climber_id).first()


def create_climber(db: Session, climber: ClimberEntity):
    db.add(climber)
    db.commit()
    db.refresh(climber)
    return climber


# MeasurementDevice CRUD Operations
def get_measurement_device(db: Session, measurement_device_id: int):
    return db.query(MeasurementDeviceEntity).filter(MeasurementDeviceEntity.id == measurement_device_id).first()


def create_measurement_device(db: Session, measurement_device: MeasurementDeviceEntity):
    db.add(measurement_device)
    db.commit()
    db.refresh(measurement_device)
    return measurement_device


# WorkoutType CRUD Operations
def get_workout_type(db: Session, workout_type_name: str):
    return db.query(WorkoutTypeEntity).filter(WorkoutTypeEntity.name == workout_type_name).first()


def create_workout_type(db: Session, workout_type: WorkoutTypeEntity):
    db.add(workout_type)
    db.commit()
    db.refresh(workout_type)
    return workout_type


# Workout CRUD Operations
def get_workout(db: Session, workout_id: int):
    return db.query(WorkoutEntity).filter(WorkoutEntity.id == workout_id).first()


def create_workout(db: Session, workout: WorkoutEntity):
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


# Measurement CRUD Operations
def get_measurement(db: Session, measurement_id: int):
    return db.query(MeasurementEntity).filter(MeasurementEntity.id == measurement_id).first()


def create_measurement(db: Session, measurement: MeasurementEntity):
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


# MeasuredData CRUD Operations
def get_measured_data(db: Session, measurement_id: int):
    return db.query(MeasuredDataEntity).filter(MeasuredDataEntity.measurement_id == measurement_id).all()


def create_measured_data(db: Session, measured_data: MeasuredDataEntity):
    db.add(measured_data)
    db.commit()
    db.refresh(measured_data)
    return measured_data


# CriticalForceWorkout CRUD Operations
def get_critical_force_workout(db: Session, workout_id: int):
    return db.query(CriticalForceWorkoutEntity).filter(CriticalForceWorkoutEntity.workout_id == workout_id).first()


def create_critical_force_workout(db: Session, critical_force_workout: CriticalForceWorkoutEntity):
    db.add(critical_force_workout)
    db.commit()
    db.refresh(critical_force_workout)
    return critical_force_workout


# MaxIsoStrengthWorkout CRUD Operations
def get_max_iso_strength_workout(db: Session, workout_id: int):
    return db.query(MaxIsoStrengthWorkoutEntity).filter(MaxIsoStrengthWorkoutEntity.workout_id == workout_id).first()


def create_max_iso_strength_workout(db: Session, max_iso_strength_workout: MaxIsoStrengthWorkoutEntity):
    db.add(max_iso_strength_workout)
    db.commit()
    db.refresh(max_iso_strength_workout)
    return max_iso_strength_workout