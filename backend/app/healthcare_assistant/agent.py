# backend/app/healthcare_assistant/agent.py
from typing import Dict, Any
from sqlalchemy.orm import Session
import re
import logging

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from ..config import settings
from .models import Schedule
from .prompts import get_prompt_template
from .tools import call_off_shift, reactivate_shift, update_shift_time
from .repository import save_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === LLM ===
llm = ChatOpenAI(
    model=settings.OPENROUTER_MODEL,
    openai_api_key=settings.OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0,
)

# === BIND DB TO TOOL WRAPPERS ===
def bind_db_to_tools(db: Session):
    call_off_shift.func.db = db
    reactivate_shift.func.db = db
    update_shift_time.func.db = db

tools = [call_off_shift, reactivate_shift, update_shift_time]
llm_with_tools = llm.bind_tools(tools)

prompt = get_prompt_template()
agent_chain: Runnable = prompt | llm_with_tools


def get_schedule_text(db: Session) -> str:
    shifts = db.query(Schedule).all()
    if not shifts:
        return "No shifts scheduled."
    lines = [f"ID {s.id}: {s.provider_name} ({s.shift_start.split(' ')[1]} - {s.shift_end.split(' ')[1]}) [{s.status.title()}]" for s in shifts]
    return "\n".join(lines)


def extract_shift_id(text: str) -> int | None:
    patterns = [r'\b(?:id|ID|shift)[\s\-:]*(\d+)', r'\b(\d{1,3})\b']
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            try:
                num = int(m.group(1))
                if 1 <= num <= 100:
                    return num
            except:
                continue
    return None


def find_shift_by_provider(text: str, db: Session) -> int | None:
    text_lower = text.lower()
    for s in db.query(Schedule).all():
        if s.provider_name.lower() in text_lower:
            return s.id
    return None


def detect_intent(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["not available", "call off", "sick", "cannot", "off", "cancel", "unavailable"]):
        return "call_off"
    if any(k in text_lower for k in ["reactivate", "back", "resume", "available again"]):
        return "reactivate"
    if re.search(r'\d{1,2}:?\d{0,2}\s*(?:am|pm)?', text, re.I) and any(k in text_lower for k in ["update", "change", "to", "from"]):
        return "update_time"
    return "unknown"


def extract_time(text: str):
    patterns = [
        r'(\d{1,2}):?(\d{2})?\s*(am|pm)?\s*[-–to]+\s*(\d{1,2}):?(\d{2})?\s*(am|pm)?',
        r'(\d{1,2})\s*(am|pm)\s*[-–to]+\s*(\d{1,2})\s*(am|pm)',
    ]
    text_lower = text.lower()
    for pat in patterns:
        m = re.search(pat, text_lower, re.I)
        if m:
            g = m.groups()
            start_h = int(g[0])
            start_m = int(g[1]) if g[1] else 0
            start_ampm = (g[2] or '').lower()
            end_h = int(g[3])
            end_m = int(g[4]) if g[4] else 0
            end_ampm = (g[5] or '').lower()

            def to_24(h, ampm):
                if ampm == 'pm' and h != 12:
                    h += 12
                if ampm == 'am' and h == 12:
                    h = 0
                return h

            start = f"{to_24(start_h, start_ampm):02d}:{start_m:02d}"
            end = f"{to_24(end_h, end_ampm):02d}:{end_m:02d}"
            return start, end
    return None, None


def process_intent(user_input: str, db: Session) -> Dict[str, Any]:
    logger.info(f"Input: {user_input}")
    
    bind_db_to_tools(db)

    intent = detect_intent(user_input)
    shift_id = extract_shift_id(user_input) or find_shift_by_provider(user_input, db)

    if intent == "call_off" and shift_id:
        result = call_off_shift.invoke({"shift_id": shift_id})
        return {"intent": "call_off", "response": result["message"]}

    if intent == "reactivate" and shift_id:
        result = reactivate_shift.invoke({"shift_id": shift_id})
        return {"intent": "reactivate", "response": result["message"]}

    if intent == "update_time" and shift_id:
        start, end = extract_time(user_input)
        if start and end:
            result = update_shift_time.invoke({"shift_id": shift_id, "new_start": start, "new_end": end})
            return {"intent": "update_time", "response": result["message"]}
        else:
            return {"intent": "error", "response": "Could not parse time. Use '10am to 12pm' or '10:00 - 18:00'."}

    if any(g in user_input.lower() for g in ["hi", "hello", "hey"]):
        return {"intent": "greeting", "response": "Hello! How can I assist you with scheduling today?"}

    return {"intent": "error", "response": "Try: 'Dr. Bilal is sick' or 'Call off ID 10' or 'Change ID 10 to 10:00 - 18:00'"}