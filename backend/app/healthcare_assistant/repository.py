# backend/app/healthcare_assistant/repository.py
from sqlalchemy.orm import Session
from .models import Schedule, Message


def get_all_schedules(db: Session):
    return db.query(Schedule).all()


def get_shift_by_id(db: Session, shift_id: int):
    return db.query(Schedule).filter(Schedule.id == shift_id).first()


def update_shift_status(db: Session, shift: Schedule, status: str):
    shift.status = status
    db.commit()
    db.refresh(shift)
    return shift


def update_shift_time(db: Session, shift: Schedule, new_start: str, new_end: str):
    date_part = shift.shift_start.split(" ")[0]
    shift.shift_start = f"{date_part} {new_start}"
    shift.shift_end = f"{date_part} {new_end}"
    db.commit()
    db.refresh(shift)
    return shift


def save_message(db: Session, user_message: str, assistant_response: str):
    msg = Message(user_message=user_message, assistant_response=assistant_response)
    db.add(msg)
    db.commit()
    return msg