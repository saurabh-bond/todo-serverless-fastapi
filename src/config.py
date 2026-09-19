import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENVIRONMENT", "dev")
    TABLE_NAME: str = os.getenv("DYNAMODB_TABLE", "dev-todos-table")
    ROOT_PATH: str = os.getenv("STAGE_PATH", "")

    class config:
        case_sensitive = True

settings = Settings()