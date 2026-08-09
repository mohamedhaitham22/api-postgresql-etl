from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #===============(App Settings)===============
    APP_NAME: str = "Fake Store API"
    APP_ENV: str = "development"

    #===============(API Settings)================
    API_BASE_URL: str 
    API_TIMEOUT: int = Field(default=10, gt=0)

    #===============(Database Settings)===========
    POSTGRES_HOST: str
    POSTGRES_PORT: int = Field(default=5432, gt=0)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str = "raw"

    #===============(Logging Settings)=============
    LOG_LEVEL: str = "INFO"
    LOG_DIRECTORY: str = "logs"
    LOG_FILE_NAME: str = "etl.log"

    #===============(Data Directory)===============
    RAW_DATA_DIR: str = "data/raw"
    PROCESSED_DATA_DIR: str = "data/processed"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
        )

    @property
    def DATABASE_URL(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}"
            f":{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()   

settings = get_settings()