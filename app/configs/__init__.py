from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import BASE_DIR, DBSettings


class Settings(BaseSettings, DBSettings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


conf = Settings()
