# backend/app/healthcare_assistant/service.py
from sqlalchemy.orm import Session
from .agent import process_intent
from .repository import save_message


def handle_chat_message(user_message: str, db: Session):
    """Process user message and return response + intent."""
    result = process_intent(user_message, db)
    response = result.get("response", "")
    intent = result.get("intent", "unknown")

    save_message(db, user_message, response)
    return {"response": response, "intent": intent}