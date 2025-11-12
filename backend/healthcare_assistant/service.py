# backend/healthcare-assistant/service.py
from sqlalchemy.orm import Session
from .agent import process_intent
from .repository import (
    get_shift_by_id, update_shift_status,
    update_shift_time, save_message
)

def handle_chat_message(user_message: str, db: Session):
    agent_result = process_intent(user_message, db)
    intent = agent_result["intent"]
    response = agent_result["response"]
    shift_id = agent_result["shift_id"]
    new_start = agent_result["new_start"]
    new_end = agent_result["new_end"]

    if intent == "greeting":
        response = "Hello! How can I assist you with scheduling today?"

    elif intent == "call_off" and shift_id:
        shift = get_shift_by_id(db, shift_id)
        if shift and shift.status != "called_off":
            shift = update_shift_status(db, shift, "called_off")
            response = f"Confirmed: {shift.provider_name}'s shift has been marked as called off."
        elif shift:
            response = "That shift is already called off."
        else:
            response = "Sorry, I couldn't find that provider. Please use the full name from the schedule."

    elif intent == "reactivate" and shift_id:
        shift = get_shift_by_id(db, shift_id)
        if shift and shift.status == "called_off":
            shift = update_shift_status(db, shift, "active")
            response = f"Shift reactivated! {shift.provider_name} is now active."
        elif shift:
            response = "That shift is already active."
        else:
            response = "Shift not found."

    elif intent == "update_shift_time" and shift_id and new_start and new_end:
        shift = get_shift_by_id(db, shift_id)
        if shift and shift.status != "called_off":
            old_time = f"{shift.shift_start.split(' ')[1]} – {shift.shift_end.split(' ')[1]}"
            shift = update_shift_time(db, shift, new_start, new_end)
            response = f"Shift updated! {shift.provider_name}'s time changed from {old_time} to {new_start} – {new_end}."
        elif shift:
            response = "Cannot update a called-off shift."
        else:
            response = "Shift not found."

    save_message(db, user_message, response)
    return {"response": response, "intent": intent}