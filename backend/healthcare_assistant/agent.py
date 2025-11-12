# backend/healthcare_assistant/agent.py
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from .models import Schedule
from .prompts import get_prompt_template
from app.config import settings  # Fixed: absolute import

class AgentOutput(BaseModel):
    intent: str = Field(description="Must be 'call_off', 'reactivate', 'update_shift_time', 'greeting', or 'query'")
    response: str = Field(description="Natural language response")
    shift_id: Optional[int] = Field(description="ID of shift to update", default=None)
    new_start: Optional[str] = Field(description="New start time (HH:MM)", default=None)
    new_end: Optional[str] = Field(description="New end time (HH:MM)", default=None)

llm = ChatOpenAI(
    model=settings.OPENROUTER_MODEL,
    openai_api_key=settings.OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.3,
)

structured_llm = llm.with_structured_output(AgentOutput)
prompt = get_prompt_template()
chain = prompt | structured_llm

def get_schedule_text(db: Session):
    shifts = db.query(Schedule).all()
    lines = []
    for s in shifts:
        status = "Called Off" if s.status == "called_off" else "Active"
        lines.append(f"- ID {s.id}: {s.provider_name}: {s.shift_start} to {s.shift_end} [{status}]")
    return "\n".join(lines) if lines else "No shifts scheduled."

def process_intent(user_input: str, db: Session):
    schedule_text = get_schedule_text(db)
    try:
        result = chain.invoke({"input": user_input, "schedule": schedule_text})
        return {
            "intent": result.intent,
            "response": result.response,
            "shift_id": result.shift_id,
            "new_start": result.new_start,
            "new_end": result.new_end
        }
    except Exception:
        return {"response": "I couldn't process that request. Please try rephrasing.", "intent": "error"}