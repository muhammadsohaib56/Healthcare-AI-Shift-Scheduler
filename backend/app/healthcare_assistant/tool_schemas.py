# backend/app/healthcare_assistant/tool_schemas.py
from pydantic import BaseModel


class CallOffInput(BaseModel):
    shift_id: int


class ReactivateInput(BaseModel):
    shift_id: int


class UpdateTimeInput(BaseModel):
    shift_id: int
    new_start: str  # HH:MM
    new_end: str    # HH:MM