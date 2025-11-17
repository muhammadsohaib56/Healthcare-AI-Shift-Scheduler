# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},   #It’s okay for multiple threads to share the same database connection.
    echo=False   #not print loggs (if True prints every query that runs on terminal)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:   #for inside the FastAPI Automaticlly
    db = SessionLocal()
    try:
        yield db      #pause, resume the DB open and close session automatically
    finally:
        db.close()

def create_session() -> Session:   #outside the FastAPI Manually
    return SessionLocal()