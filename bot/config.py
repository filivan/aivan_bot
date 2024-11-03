import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

logger.add("log/log.debug", level="DEBUG")
logger.add("log/log.warn", level="WARNING")


class Settings(BaseSettings):
    GROQ_API_KEY: str
    BOT_TOKEN: str
    ACCESS_PASSWORD: str
    SPEECH_MODEL: str = "whisper-large-v3-turbo"
    CHAT_COMPLETION_MODEL: str = "llama-3.2-90b-vision-preview"

    if os.path.exists(".env"):
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
