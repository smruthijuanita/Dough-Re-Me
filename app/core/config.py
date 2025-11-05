"""Application configuration using Pydantic BaseSettings."""
from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional


class Settings(BaseSettings):
    # Application
    app_name: str = "Dough-Re-Me Bakery"
    debug: bool = True
    
    # Database - PostgreSQL
    postgres_server: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "dough_re_me"
    postgres_port: str = "5432"
    database_url: Optional[PostgresDsn] = None
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_server"),
            port=values.get("postgres_port"),
            path=f"/{values.get('postgres_db') or ''}",
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
