from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ResumeIQ AI"
    APP_VERSION: str = "1.0.0"

    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()