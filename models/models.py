from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func

from database import Base


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

class MeasurementDevice(Base):
    __tablename__ = "measurement_device"

    id = Column(Integer, primary_key=True, index=True)
    sample_rate_hz = Column(Integer)

class WorkoutType(Base):
    __tablename__ = "workout_type"

    name = Column(String, primary_key=True, index=True)
    description = Column(String)
    sets_number = Column(Integer)
    set_pause = Column(Integer)
    repetitions = Column(Integer)
    repetition_active = Column(Integer)
    repetition_pause = Column(Integer)

class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    workout_name = Column(String, ForeignKey("workout_type.name"))
    climber_id = Column(Integer, ForeignKey("climber.id"), index=True)
    body_weight = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Measurement(Base):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout.id"))
    measurement_device_id = Column(Integer, ForeignKey("measurement_device.id"))
    current_repetition = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class MeasuredData(Base):
    __tablename__ = "measured_data"

    measurement_id = Column(Integer, ForeignKey("measurement.id"), primary_key=True, index=True)
    iteration = Column(Integer, primary_key=True)
    weight = Column(Float, primary_key=True)

class CriticalForceWorkout(Base):
    __tablename__ = "critical_force_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    critical_force = Column(Float)
    w_prime = Column(Float)
    max_force = Column(Float)

class MaxIsoStrengthWorkout(Base):
    __tablename__ = "max_iso_strength_workout"

    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True, index=True)
    max_force = Column(Float)