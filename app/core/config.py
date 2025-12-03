"""Application configuration using Pydantic BaseSettings."""
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from typing import Optional


class Settings(BaseSettings):
    # Application
    app_name: str = "Dough-Re-Me Bakery"
    debug: bool = True
    
    # Database - PostgreSQL
    postgres_server: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "elvis"
    postgres_db: str = "Doughreme"
    postgres_port: str = "5432"
    database_url: Optional[str] = None
    
    # SMTP Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    sender_email: str = ""
    
    @property
    def get_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

    model_config = {
        "env_file": ".env",
        # Allow common uppercase env names (POSTGRES_PORT, APP_NAME, DEBUG)
        "case_sensitive": False,
        # Ignore extra env entries instead of forbidding them (avoids extra_forbidden)
        "extra": "ignore",
    }


settings = Settings()
