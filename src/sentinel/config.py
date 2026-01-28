"""
Configuration management using Pydantic Settings
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyHttpUrl


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # WAHA API Configuration
    WAHA_API_URL: str = Field(default="https://waha.compumax.tech")
    WAHA_API_KEY: str = Field(default="")
    WAHA_SESSION_NAME: str = Field(default="default")
    WAHA_TIMEOUT: int = Field(default=30)

    # Database Configuration
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/sentinel_waha")
    DATABASE_POOL_SIZE: int = Field(default=10)
    DATABASE_MAX_OVERFLOW: int = Field(default=20)

    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_PASSWORD: str = Field(default="")

    # Application Settings
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)
    APP_PORT: int = Field(default=8000)
    APP_HOST: str = Field(default="0.0.0.0")
    SECRET_KEY: str = Field(default="change_this_in_production")

    # Feature Flags
    ENABLE_AUTO_RESPONSE: bool = Field(default=True)
    ENABLE_ANALYTICS: bool = Field(default=True)
    ENABLE_WEBHOOKS: bool = Field(default=True)
    ENABLE_INTENT_CLASSIFICATION: bool = Field(default=True)

    # Response Engine Settings
    RESPONSE_DELAY_MIN: int = Field(default=2)
    RESPONSE_DELAY_MAX: int = Field(default=5)
    ENABLE_TYPING_INDICATOR: bool = Field(default=True)
    TYPING_SPEED_CHARS_PER_SECOND: int = Field(default=40)
    MAX_AUTO_RESPONSES_PER_CONVERSATION: int = Field(default=3)
    HUMAN_HANDOFF_AFTER_MINUTES: int = Field(default=30)

    # Intent Classification
    INTENT_HIGH_THRESHOLD: float = Field(default=0.8)
    INTENT_MEDIUM_THRESHOLD: float = Field(default=0.5)
    HIGH_INTENT_KEYWORDS: str = Field(
        default="precio,costo,pago,comprar,envío,delivery,disponible,stock"
    )
    LOW_INTENT_KEYWORDS: str = Field(
        default="hola,hello,hi,hey,buenos días,buenas tardes"
    )

    # Webhooks
    WEBHOOK_SECRET: str = Field(default="")
    WEBHOOK_URL: str = Field(default="")
    WEBHOOK_RETRY_ATTEMPTS: int = Field(default=3)

    # Analytics & Monitoring
    METRICS_COLLECTION_INTERVAL: int = Field(default=60)
    DASHBOARD_REFRESH_RATE: int = Field(default=30)
    ENABLE_GOOGLE_ANALYTICS: bool = Field(default=False)
    GOOGLE_ANALYTICS_ID: str = Field(default="")

    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")
    LOG_FILE: str = Field(default="logs/sentinel.log")
    LOG_MAX_SIZE: int = Field(default=10485760)
    LOG_BACKUP_COUNT: int = Field(default=5)

    # Business Rules
    BUSINESS_HOURS_START: str = Field(default="09:00")
    BUSINESS_HOURS_END: str = Field(default="18:00")
    BUSINESS_TIMEZONE: str = Field(default="America/Mexico_City")
    TARGET_FIRST_RESPONSE_TIME: int = Field(default=5)
    TARGET_AVERAGE_RESPONSE_TIME: int = Field(default=10)

    # Extraction Settings
    EXTRACTION_BATCH_SIZE: int = Field(default=100)
    EXTRACTION_MAX_RETRIES: int = Field(default=3)
    EXTRACTION_START_DATE: str = Field(default="2024-01-01")
    EXTRACTION_END_DATE: str = Field(default="2026-01-28")

    # Security
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    RATE_LIMIT_PER_HOUR: int = Field(default=1000)
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "https://compumax.tech"]
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)

    # Notification Settings
    ALERT_PHONE_NUMBER: str = Field(default="")
    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    ALERT_EMAIL: str = Field(default="")

    # Advanced Settings
    ML_MODEL_PATH: str = Field(default="models/intent_classifier.pkl")
    ML_MODEL_VERSION: str = Field(default="1.0.0")
    ML_RETRAIN_THRESHOLD_DAYS: int = Field(default=30)
    QUEUE_MAX_SIZE: int = Field(default=1000)
    QUEUE_WORKER_THREADS: int = Field(default=4)
    CACHE_TTL_SHORT: int = Field(default=300)
    CACHE_TTL_MEDIUM: int = Field(default=3600)
    CACHE_TTL_LONG: int = Field(default=86400)

    @property
    def high_intent_keywords_list(self) -> List[str]:
        """Get high intent keywords as list"""
        return [k.strip() for k in self.HIGH_INTENT_KEYWORDS.split(",")]

    @property
    def low_intent_keywords_list(self) -> List[str]:
        """Get low intent keywords as list"""
        return [k.strip() for k in self.LOW_INTENT_KEYWORDS.split(",")]


# Create global settings instance
settings = Settings()
