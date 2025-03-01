from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# SQLAlchemy Models (Database)
class Climber(Base):
    __tablename__ = "climber"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    span = Column(Float)
    route_grade = Column(String)
    boulder_grade = Column(String)

    workouts = relationship("Workout", back_populates="climber")


class MeasurementDevice(Base):
    __tablename__ = "measurement_device"

    id = Column(Integer, primary_key=True, index=True)
    sample_rate_hz = Column(Integer)
    measurements = relationship("Measurement", back_populates="measurement_device")


class WorkoutType(Base):
    __tablename__ = "workout_type"

    name = Column(String, primary_key=True, index=True)
    description = Column(String)
    sets_number = Column(Integer)
    set_pause = Column(Integer)
    repetitions = Column(Integer)
    repetition_active = Column(Integer)
    repetition_pause = Column(Integer)
    workouts = relationship("Workout", back_populates="workout_type")


class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    workout_name = Column(String, ForeignKey("workout_type.name"))
    climber_id = Column(Integer, ForeignKey("climber.id"), index=True)
    body_weight = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    climber = relationship("Climber", back_populates="workouts")
    workout_type = relationship("WorkoutType", back_populates="workouts")
    measurements = relationship("Measurement", back_populates="workout")
    critical_force_workouts = relationship("CriticalForceWorkout", back_populates="workout")
    max_iso_strength_workouts = relationship("MaxIsoStrengthWorkout", back_populates="workout")


class Measurement(Base):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout.id"))
    measurement_device_id = Column(Integer, ForeignKey("measurement_device.id"))
    current_repetition = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    workout = relationship("Workout", back_populates="measurements")
    measurement_device = relationship("MeasurementDevice", back_populates="measurements")
    measured_data = relationship("MeasuredData", back_populates="measurement")


class MeasuredData(Base):
    __tablename__ = "measured_data"

    measurement_id = Column(Integer, ForeignKey("measurement.id"), primary_key=True, index=True)
    iteration = Column(Integer, primary_key=True)
    weight = Column(Float)
    measurement = relationship("Measurement", back_populates="measured_data")


class CriticalForceWorkout(Base):
    __tablename__ = "critical_force_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    critical_force = Column(Float)
    w_prime = Column(Float)
    max_force = Column(Float)
    workout = relationship("Workout", back_populates="critical_force_workouts")


class MaxIsoStrengthWorkout(Base):
    __tablename__ = "max_iso_strength_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    max_force = Column(Float)
    workout = relationship("Workout", back_populates="max_iso_strength_workouts")


# Pydantic Models (API)
class ClimberBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str
    height: float
    span: float
    route_grade: str
    boulder_grade: str
    id : Optional[int] = None

    class Config:
        from_attributes = True


class ClimberCreate(ClimberBase):
    pass


class MeasurementDeviceBase(BaseModel):
    sample_rate_hz: int
    id : Optional[int] = None

    class Config:
        from_attributes = True


class MeasurementDeviceCreate(MeasurementDeviceBase):
    pass


class WorkoutTypeBase(BaseModel):
    name: str
    description: str
    sets_number: int
    set_pause: int
    repetitions: int
    repetition_active: int
    repetition_pause: int

    class Config:
        from_attributes = True


class WorkoutTypeCreate(WorkoutTypeBase):
    pass


class WorkoutBase(BaseModel):
    workout_name: str
    climber_id: int
    body_weight: float
    created_at: datetime
    updated_at: datetime
    id : Optional[int] = None

    class Config:
        from_attributes = True


class WorkoutCreate(WorkoutBase):
    pass


class MeasurementBase(BaseModel):
    workout_id: int
    measurement_device_id: int
    current_repetition: int
    created_at: datetime
    updated_at: datetime
    id : Optional[int] = None

    class Config:
        from_attributes = True


class MeasurementCreate(MeasurementBase):
    pass


class MeasuredDataBase(BaseModel):
    measurement_id: int
    iteration: int
    weight: float

    class Config:
        from_attributes = True


class MeasuredDataCreate(MeasuredDataBase):
    pass


class CriticalForceWorkoutBase(BaseModel):
    critical_force: float
    w_prime: float
    max_force: float
    workout_id: int

    class Config:
        from_attributes = True


class CriticalForceWorkoutCreate(CriticalForceWorkoutBase):
    pass


class MaxIsoStrengthWorkoutBase(BaseModel):
    max_force: float
    workout_id: int

    class Config:
        from_attributes = True


class MaxIsoStrengthWorkoutCreate(MaxIsoStrengthWorkoutBase):
    pass