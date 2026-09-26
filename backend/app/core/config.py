from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Enterprise Capability & Delivery Governance Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    DEMO_MODE: bool = True

    # Database — set DATABASE_URL directly to override (e.g. sqlite:///./governance.db)
    DATABASE_URL: str = "sqlite:///./governance.db"

    # MySQL settings (used only when DATABASE_URL is not overridden)
    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_NAME: str = "governance_db"
    DB_USER: str = "governance_user"
    DB_PASSWORD: str = "governance_pass"

    # Auth0
    AUTH0_DOMAIN: str = ""
    AUTH0_AUDIENCE: str = ""
    AUTH0_NAMESPACE: str = "https://governance/"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # IBM watsonx.ai
    WATSONX_API_KEY: Optional[str] = None
    WATSONX_PROJECT_ID: Optional[str] = None
    WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_MODEL_ID: str = "ibm/granite-3-3-8b-instruct"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
