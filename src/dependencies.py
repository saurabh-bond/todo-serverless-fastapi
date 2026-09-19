from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import urllib.request
import json
from src.config import settings

# This forces the "Authorize" padlock button to show up inside Swagger UI docs
security = HTTPBearer()

# Cache the Cognito public keys globally at application level to avoid hot cold starts overhead
jwks_cache = None


def get_cognito_public_keys():
    global jwks_cache
    if not settings.COGNITO_USER_POOL_ID or not settings.COGNITO_APP_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cognito user pool and client are not configured."
        )

    if not jwks_cache:
        try:
            with urllib.request.urlopen(settings.COGNITO_JWKS_URL) as response:
                jwks_cache = json.loads(response.read().decode("utf-8"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not bootstrap authorization validation keys."
            )
    return jwks_cache


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    jwks=Depends(get_cognito_public_keys)
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_str = token.credentials
        header = jwt.get_unverified_header(token_str)
        kid = header.get("kid")

        # Find the matching public key from the Cognito JWKS payload
        key_index = -1
        for i, key in enumerate(jwks.get("keys", [])):
            if kid == key.get("kid"):
                key_index = i
                break
        if key_index == -1:
            raise credentials_exception

        payload = jwt.decode(
            token_str,
            jwks["keys"][key_index],
            algorithms=["RS256"],
            audience=settings.COGNITO_APP_CLIENT_ID,
            issuer=settings.COGNITO_ISSUER_URL
        )

        username: str = payload.get("cognito:username") or payload.get("username") or payload.get("sub")
        if username is None:
            raise credentials_exception

        return {"username": username, "email": payload.get("email")}

    except JWTError:
        raise credentials_exception
