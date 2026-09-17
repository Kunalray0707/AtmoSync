"""Application configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",
    }

    # Application
    APP_NAME: str = "AtmoSync"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # PostgreSQL
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/atmosync"
    DATABASE_URL_SYNC: str = "postgresql://user:password@localhost:5432/atmosync"

    # JWT
    SECRET_KEY: str = "replace-me-with-a-long-random-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_IOT_SENSOR: str = "iot_sensor_data"
    KAFKA_TOPIC_COMMODITY_PRICE: str = "commodity_prices"
    KAFKA_CONSUMER_GROUP: str = "atmosync_consumer_group"

    # Snowflake
    SNOWFLAKE_ACCOUNT: Optional[str] = None
    SNOWFLAKE_USER: Optional[str] = None
    SNOWFLAKE_PASSWORD: Optional[str] = None
    SNOWFLAKE_WAREHOUSE: Optional[str] = None
    SNOWFLAKE_DATABASE: Optional[str] = None
    SNOWFLAKE_SCHEMA: Optional[str] = None

    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB


settings = Settings()
