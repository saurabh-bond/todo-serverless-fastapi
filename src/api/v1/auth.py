from fastapi import APIRouter, Depends, status
from src.models.auth_schema import UserRegister, UserLogin, TokenResponse
from src.services.cognito_service import CognitoService

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserRegister, service: CognitoService = Depends()):
    service.register_user(email=payload.email, password=payload.password)
    return {"message": "Signup successful. Please confirm your email in Cognito console before logging in."}

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, service: CognitoService = Depends()):
    return service.login_user(email=payload.email, password=payload.password)
