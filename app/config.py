import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()

database_url = settings.database_url.strip() if settings.database_url else ""

if not database_url or database_url.startswith("http://") or database_url.startswith("https://"):
    print("[config] INFO: DATABASE_URL is not set or invalid. Using SQLite for development.")
    settings.database_url = "sqlite:///./pair_programming.db"
elif database_url.startswith("postgresql://"):
    settings.database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    print(f"[config] INFO: Using PostgreSQL with psycopg3 driver.")
elif database_url.startswith("postgresql+psycopg://"):
    print(f"[config] INFO: Using PostgreSQL with psycopg3 driver.")
else:
    settings.database_url = database_url

if not settings.gemini_api_key:
    print("[config] WARNING: GEMINI_API_KEY is not set. Autocomplete will use mocked suggestions.")
