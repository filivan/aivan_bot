from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GROQ_API_KEY: str
    BOT_TOKEN: str
    # @property
    # def GROQ_API_KEY(self):
    #     return self.GROQ_API_KEY

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
settings = Settings()