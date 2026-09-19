import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    ENV: str = ENVIRONMENT
    ROOT_PATH: str = os.getenv("STAGE_PATH", "")
    TABLE_NAME: str = os.getenv("DYNAMODB_TABLE", "dev-todos-table")

    # Cognito configuration passed in from the SAM template
    COGNITO_USER_POOL_ID: str = os.getenv("COGNITO_USER_POOL_ID", "")
    COGNITO_APP_CLIENT_ID: str = os.getenv("COGNITO_APP_CLIENT_ID", "")
    COGNITO_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    @property
    def COGNITO_ISSUER_URL(self) -> str:
        if not self.COGNITO_USER_POOL_ID:
            return ""
        return f"https://cognito-idp.{self.COGNITO_REGION}.amazonaws.com/{self.COGNITO_USER_POOL_ID}"

    @property
    def COGNITO_JWKS_URL(self) -> str:
        if not self.COGNITO_USER_POOL_ID:
            return ""
        return f"{self.COGNITO_ISSUER_URL}/.well-known/jwks.json"


settings = Settings()