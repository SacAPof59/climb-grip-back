# models.py - Fixed version
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, joinedload
from database.database import Base
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Tuple


# SQLAlchemy Models (Database)
class ClimberEntity(Base):
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

    workouts = relationship("WorkoutEntity", back_populates="climber")


class MeasurementDeviceEntity(Base):
    __tablename__ = "measurement_device"

    id = Column(Integer, primary_key=True, index=True)
    sample_rate_hz = Column(Integer)
    measurements = relationship("MeasurementEntity", back_populates="measurement_device")


class WorkoutTypeEntity(Base):
    __tablename__ = "workout_type"

    name = Column(String, primary_key=True, index=True)
    description = Column(String)
    sets_number = Column(Integer)
    set_pause = Column(Integer)
    repetitions = Column(Integer)
    repetition_active = Column(Integer)
    repetition_pause = Column(Integer)
    workouts = relationship("WorkoutEntity", back_populates="workout_type")


class WorkoutEntity(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    workout_name = Column(String, ForeignKey("workout_type.name"))
    climber_id = Column(Integer, ForeignKey("climber.id"), index=True)
    body_weight = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    climber = relationship("ClimberEntity", back_populates="workouts")
    workout_type = relationship("WorkoutTypeEntity", back_populates="workouts")
    measurements = relationship("MeasurementEntity", back_populates="workout")
    critical_force_workouts = relationship("CriticalForceWorkoutEntity", back_populates="workout")
    max_iso_strength_workouts = relationship("MaxIsoStrengthWorkoutEntity", back_populates="workout")


class MeasurementEntity(Base):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout.id"))
    measurement_device_id = Column(Integer, ForeignKey("measurement_device.id"))
    current_repetition = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    workout = relationship("WorkoutEntity", back_populates="measurements")
    measurement_device = relationship("MeasurementDeviceEntity", back_populates="measurements")
    measured_data = relationship("MeasuredDataEntity", back_populates="measurement")


class MeasuredDataEntity(Base):
    __tablename__ = "measured_data"

    measurement_id = Column(Integer, ForeignKey("measurement.id"), primary_key=True, index=True)
    iteration = Column(Integer, primary_key=True)
    weight = Column(Float)
    measurement = relationship("MeasurementEntity", back_populates="measured_data")


class CriticalForceWorkoutEntity(Base):
    __tablename__ = "critical_force_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    critical_force = Column(Float)
    w_prime = Column(Float)
    max_force = Column(Float)
    workout = relationship("WorkoutEntity", back_populates="critical_force_workouts")


class MaxIsoStrengthWorkoutEntity(Base):
    __tablename__ = "max_iso_strength_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    max_force = Column(Float)
    workout = relationship("WorkoutEntity", back_populates="max_iso_strength_workouts")


# Pydantic Models (API)
class MeasurementDeviceBase(BaseModel):
    sample_rate_hz: int
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MeasuredDataBase(BaseModel):
    measurement_id: int
    iteration: int
    weight: float

    model_config = ConfigDict(from_attributes=True)


class ClimberBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str
    height: float
    span: float
    route_grade: str
    boulder_grade: str
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ClimberCreate(ClimberBase):
    pass


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

    model_config = ConfigDict(from_attributes=True)


class WorkoutTypeCreate(WorkoutTypeBase):
    pass


# Simplified measurement model for API responses
class MeasurementResponse(BaseModel):
    id: int
    workout_id: int
    measurement_device_id: int
    current_repetition: int
    created_at: datetime
    updated_at: datetime
    measurement_device: Optional[MeasurementDeviceBase] = None
    measured_data_for_graph: Optional[List[Tuple[float, float]]] = None #add this

    model_config = ConfigDict(from_attributes=True)


class MeasurementCreate(BaseModel):
    workout_id: int
    measurement_device_id: int
    current_repetition: int
    created_at: datetime
    updated_at: datetime


class WorkoutBase(BaseModel):
    workout_name: str
    climber_id: int
    body_weight: float
    created_at: datetime
    updated_at: datetime
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutRead(WorkoutBase):
    id: int
    measurements: Optional[List[MeasurementResponse]] = None

    model_config = ConfigDict(from_attributes=True)


class MeasuredDataCreate(MeasuredDataBase):
    pass


class CriticalForceWorkoutBase(BaseModel):
    critical_force: float
    w_prime: float
    max_force: float
    workout_id: int

    model_config = ConfigDict(from_attributes=True)


class CriticalForceWorkoutCreate(CriticalForceWorkoutBase):
    pass


class MaxIsoStrengthWorkoutBase(BaseModel):
    max_force: float
    workout_id: int

    model_config = ConfigDict(from_attributes=True)


class MaxIsoStrengthWorkoutCreate(MaxIsoStrengthWorkoutBase):
    pass