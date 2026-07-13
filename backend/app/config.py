from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "OmniScene"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/omniscene")
    
    # API Keys
    GROQ_API_KEY: str | None = None
    
    # Auth
    SECRET_KEY: str = "supersecretkey123" # In production, this should be a secure random string
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Confidence thresholds
    CONFIDENCE_HIGH: float = 0.85
    CONFIDENCE_MEDIUM: float = 0.60
    CONFIDENCE_LOW: float = 0.30
    
    # Paths
    MODEL_DIR: str = "../data/models"
    INDEX_DIR: str = "../data/indexes"
    STATIC_DIR: str = "static"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
