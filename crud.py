from sqlalchemy.orm import Session
from models.models import Climber


def create_climber(db: Session, climber: Climber):
    db.add(climber)
    db.commit()
    db.refresh(climber)
    return climber