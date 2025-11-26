import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()

if not settings.database_url:
    print("[config] WARNING: DATABASE_URL is not set. Supabase connection will fail.")

if not settings.gemini_api_key:
    print("[config] WARNING: GEMINI_API_KEY is not set. Autocomplete will fail later.")
