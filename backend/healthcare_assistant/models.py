# backend/healthcare-assistant/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# === SQLAlchemy Models ===
class Base(DeclarativeBase):
    pass

class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String, index=True)
    shift_start = Column(String)
    shift_end = Column(String)
    status = Column(String, default="active")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    assistant_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# === Pydantic Schema (moved from schemas.py) ===
class ScheduleOut(BaseModel):
    id: int
    provider_name: str
    shift_start: str
    shift_end: str
    status: Optional[str] = "active"

    class Config:
        from_attributes = True