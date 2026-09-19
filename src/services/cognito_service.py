import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from src.config import settings

class CognitoService:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=settings.COGNITO_REGION)

    def register_user(self, email: str, password: str):
        try:
            response = self.client.sign_up(
                ClientId=settings.COGNITO_APP_CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": email}]
            )
            return response
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.response["Error"]["Message"]
            )

    def login_user(self, email: str, password: str):
        try:
            response = self.client.initiate_auth(
                ClientId=settings.COGNITO_APP_CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password
                }
            )
            auth_result = response["AuthenticationResult"]
            return {
                "access_token": auth_result["AccessToken"],
                "id_token": auth_result["IdToken"],
                "refresh_token": auth_result["RefreshToken"]
            }
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.response["Error"]["Message"]
            )
