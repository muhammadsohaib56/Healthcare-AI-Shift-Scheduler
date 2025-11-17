# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .healthcare_assistant.models import Base, Schedule
from .healthcare_assistant.router import router
import uvicorn

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare AI Scheduling Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if db.query(Schedule).count() == 0:
            sample = [
                Schedule(provider_name="Dr. Ahmed", shift_start="2025-11-12 09:00", shift_end="2025-11-12 17:00"),
                Schedule(provider_name="Nurse Sara", shift_start="2025-11-13 14:00", shift_end="2025-11-13 22:00"),
                Schedule(provider_name="Dr. Khan", shift_start="2025-11-14 08:00", shift_end="2025-11-14 16:00"),
                Schedule(provider_name="Dr. Fatima", shift_start="2025-11-12 10:00", shift_end="2025-11-12 18:00"),
                Schedule(provider_name="Dr. Ali", shift_start="2025-11-13 08:00", shift_end="2025-11-13 16:00"),
                Schedule(provider_name="Dr. Zain", shift_start="2025-11-14 14:00", shift_end="2025-11-14 22:00"),
                Schedule(provider_name="Dr. Hamza", shift_start="2025-11-14 13:00", shift_end="2025-11-14 15:00"),
                Schedule(provider_name="Dr. Ahsan", shift_start="2025-11-14 15:00", shift_end="2025-11-14 17:00"),
                Schedule(provider_name="Dr. Naeem", shift_start="2025-11-14 18:00", shift_end="2025-11-14 21:00"),
                Schedule(provider_name="Dr. Bilal", shift_start="2025-11-15 09:00", shift_end="2025-11-15 17:00"),
            ]
            db.add_all(sample)
            db.commit()
            print(f"Sample data seeded: {len(sample)} shifts")
        else:
            print("Database already has data. Skipping seed.")
    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)