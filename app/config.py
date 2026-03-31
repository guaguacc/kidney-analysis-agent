import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Kidney Agent")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5")
    OPENAI_TIMEOUT: float = float(os.getenv("OPENAI_TIMEOUT", "30"))


settings = Settings()


def get_settings() -> Settings:
    return settings