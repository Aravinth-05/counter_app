"""
config.py -- Application configuration

Reads database connection details from environment variables.
This is how real apps work: you NEVER hardcode passwords or hostnames
in your code. Instead, the environment tells the app where to connect.

In Phase 1: you set these in your terminal before running the app.
In Phase 3 (Docker): docker-compose sets them automatically.
In Phase 4 (K8s): ConfigMaps and Secrets set them.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # These map to environment variables (case-insensitive)
    # e.g., DB_HOST env var -> db_host field
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "counter_db"
    db_user: str = "counter_user"
    db_password: str = "counter_pass"

    @property
    def database_url(self) -> str:
        """Build the full connection string PostgreSQL needs."""
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


# Single instance used across the app
settings = Settings()
