from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent


class DatabaseSettings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: str
    postgres_host: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    model_config = SettingsConfigDict(env_file=ENV_PATH / ".env", extra="ignore")


class TelegramSettings(BaseSettings):
    bot_token: str

    model_config = SettingsConfigDict(env_file=ENV_PATH / ".env", extra="ignore")


class AiChatSettings(BaseSettings):
    ai_api_key: str
    ai_base_url: str

    model_config = SettingsConfigDict(env_file=ENV_PATH / ".env", extra="ignore")


class Settings(BaseSettings):
    database: DatabaseSettings
    telegram: TelegramSettings
    ai: AiChatSettings()


settings = Settings(
    database=DatabaseSettings(),
    telegram=TelegramSettings(),
    ai=AiChatSettings(),
)
