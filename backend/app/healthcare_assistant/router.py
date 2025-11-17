# backend/app/healthcare_assistant/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .service import handle_chat_message
from .repository import get_all_schedules
from .schema import ScheduleOut

router = APIRouter()

@router.get("/api/schedule", response_model=List[ScheduleOut])
def get_schedule(db: Session = Depends(get_db)):
    try:
        return get_all_schedules(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")

@router.post("/api/chat")
def chat(request: dict, db: Session = Depends(get_db)):
    user_message = request.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")
    return handle_chat_message(user_message, db)