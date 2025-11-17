# backend/app/healthcare_assistant/tools.py
import re
from typing import Dict, Any
from sqlalchemy.orm import Session
from langchain_core.tools import StructuredTool
from .repository import (
    get_shift_by_id,
    update_shift_status,
    update_shift_time as repo_update_shift_time  # <-- ALIAS
)
from .tool_schemas import CallOffInput, ReactivateInput, UpdateTimeInput


# === TOOL FUNCTIONS ===
def _call_off(shift_id: int, db: Session) -> Dict[str, Any]:
    shift = get_shift_by_id(db, shift_id)
    if not shift:
        return {"success": False, "message": "Shift not found."}
    if shift.status == "called_off":
        return {"success": False, "message": "That shift is already called off."}
    update_shift_status(db, shift, "called_off")
    return {"success": True, "message": f"{shift.provider_name}'s shift has been marked as called off."}


def _reactivate(shift_id: int, db: Session) -> Dict[str, Any]:
    shift = get_shift_by_id(db, shift_id)
    if not shift:
        return {"success": False, "message": "Shift not found."}
    if shift.status != "called_off":
        return {"success": False, "message": "That shift is already active."}
    update_shift_status(db, shift, "active")
    return {"success": True, "message": f"{shift.provider_name} is now active."}


def _update_time(shift_id: int, new_start: str, new_end: str, db: Session) -> Dict[str, Any]:
    shift = get_shift_by_id(db, shift_id)
    if not shift:
        return {"success": False, "message": "Shift not found."}
    if shift.status == "called_off":
        return {"success": False, "message": "Cannot update a called-off shift."}
    
    if not (re.match(r"^\d{2}:\d{2}$", new_start) and re.match(r"^\d{2}:\d{2}$", new_end)):
        return {"success": False, "message": "Invalid time format. Use HH:MM (24-hour)."}
    
    old_start = shift.shift_start.split(" ")[1]
    old_end = shift.shift_end.split(" ")[1]
    
    # Use REPOSITORY function, NOT the tool!
    repo_update_shift_time(db, shift, new_start, new_end)
    
    return {
        "success": True,
        "message": f"{shift.provider_name}'s time changed from {old_start} – {old_end} to {new_start} – {new_end}."
    }


# === TOOL FACTORY ===
def create_tool(func, name: str, description: str, schema):
    def tool_wrapper(**kwargs):
        db = getattr(tool_wrapper, "db", None)
        if db is None:
            raise RuntimeError("Database session not bound to tool.")
        return func(**kwargs, db=db)
    
    tool = StructuredTool.from_function(
        func=tool_wrapper,
        name=name,
        description=description,
        args_schema=schema,
    )
    return tool


# === Create Tools ===
call_off_shift = create_tool(
    func=_call_off,
    name="call_off_shift",
    description="Mark a shift as called off using its exact ID.",
    schema=CallOffInput,
)

reactivate_shift = create_tool(
    func=_reactivate,
    name="reactivate_shift",
    description="Reactivate a called-off shift using its ID.",
    schema=ReactivateInput,
)

update_shift_time = create_tool(
    func=_update_time,
    name="update_shift_time",
    description="Update shift time (HH:MM) using shift ID.",
    schema=UpdateTimeInput,
)