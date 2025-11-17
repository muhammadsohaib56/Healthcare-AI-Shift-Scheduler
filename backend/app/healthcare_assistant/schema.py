# backend/app/healthcare_assistant/schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# === Agent Output Schema ===
class AgentOutput(BaseModel):
    intent: str = Field(description="Must be 'call_off', 'reactivate', 'update_shift_time', 'greeting', or 'query'")
    response: str = Field(description="Natural language response")
    shift_id: Optional[int] = Field(description="ID of shift to update", default=None)
    new_start: Optional[str] = Field(description="New start time (HH:MM)", default=None)
    new_end: Optional[str] = Field(description="New end time (HH:MM)", default=None)

# === Schedule Schemas ===
class ScheduleBase(BaseModel):
    provider_name: str
    shift_start: str
    shift_end: str
    status: Optional[str] = "active"

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    provider_name: Optional[str] = None
    shift_start: Optional[str] = None
    shift_end: Optional[str] = None
    status: Optional[str] = None

class ScheduleOut(ScheduleBase):
    id: int

    class Config:
        from_attributes = True

# === Message Schemas ===
class MessageBase(BaseModel):
    user_message: str
    assistant_response: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True