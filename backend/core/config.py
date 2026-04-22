from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    APP_NAME: str = "AI Resume Analyzer"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["*"]
    TOP_K_KEYWORDS: int = 15
    SIMILARITY_WEIGHT: float = 0.7
    KEYWORD_WEIGHT: float = 0.3


settings = Settings()
