import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "env_files", ".env"
        )

        env_file_encoding = "utf-8"


settings = Settings()
