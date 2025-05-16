from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # Qwen3 settings
    QWEN3_API_URL: str = os.getenv("QWEN3_API_URL", "http://localhost:11434/api/generate")
    QWEN3_MODEL: str = os.getenv("QWEN3_MODEL", "qwen:7b")
    QWEN3_TIMEOUT: int = int(os.getenv("QWEN3_TIMEOUT", "60"))

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()
