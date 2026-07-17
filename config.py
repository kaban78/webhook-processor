from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://mongo:27017"
    MONGODB_DB: str = "webhooks"
    REDIS_URL: str = "redis://redis:6379/0"
    WEBHOOK_SECRET: str = "change-me"
    REDIS_QUEUE: str = "webhook_queue"
    REDIS_PROCESSING_QUEUE: str = "webhook_queue_processing"

    class Config:
        env_file = ".env"

settings = Settings()
