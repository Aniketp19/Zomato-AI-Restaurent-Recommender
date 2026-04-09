from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Zomato AI Recommender", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_port: int = Field(default=8000, alias="APP_PORT")

    hf_dataset_id: str = Field(
        default="ManikaSaini/zomato-restaurant-recommendation", alias="HF_DATASET_ID"
    )
    hf_dataset_split: str = Field(default="train", alias="HF_DATASET_SPLIT")

    sqlite_path: str = Field(default="data/restaurants.db", alias="SQLITE_PATH")
    critical_null_threshold: float = Field(default=0.35, alias="CRITICAL_NULL_THRESHOLD")
    max_allowed_duplicate_ratio: float = Field(
        default=0.4, alias="MAX_ALLOWED_DUPLICATE_RATIO"
    )
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.1-8b-instant", alias="GROQ_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlite_file(self) -> Path:
        return Path(self.sqlite_path)


settings = Settings()
