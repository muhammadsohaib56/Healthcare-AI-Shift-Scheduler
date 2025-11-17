# backend/app/config.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "openai/gpt-oss-120b"
    DATABASE_URL: str = "sqlite:///schedule.db"

    model_config = {
        "env_file": "../.env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()