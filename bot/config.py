import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

os.makedirs(name="log", exist_ok=True)
logger.add("log/log.debug", level="DEBUG")
logger.add("log/log.warn", level="WARNING")


class Settings(BaseSettings):
    GROQ_API_KEY: str
    BOT_TOKEN: str
    ACCESS_PASSWORD: str
    CHAT_COMPLETION_MODEL: str = "meta-llama/llama-4-maverick-17b-128e-instruct"
    SPEECH_TEXT_MODEL: str = "whisper-large-v3-turbo"
    TEXT_SPEECH_MODEL: str = "playai-tts"
    TEXT_SPEECH_MODEL_VOICE: str = "Atlas-PlayAI"
    VISION_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    AUTHORIZED_USERS_ID: set = {450267784}
    AUTHORIZED_CHATS_ID: set = {-1002263878476}

    if os.path.exists(".env"):
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
