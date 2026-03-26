import logging
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.core.auth import create_access_token, verify_password
from app.core.config import settings
from app.schemas.auth import LoginRequest, TokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login with username and password",
)
def login(payload: LoginRequest) -> TokenResponse:
    logger.info("Login attempted for user: %s", payload.username)
    
    # Demo user validation
    if payload.username != settings.DEMO_USERNAME:
        logger.warning("Login failed: invalid username %s", payload.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if payload.password != settings.DEMO_PASSWORD:
        logger.warning("Login failed: invalid password for user %s", payload.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    # Create access token
    access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    access_token = create_access_token(
        data={"sub": payload.username}, expires_delta=access_token_expires
    )
    
    logger.info("Login successful for user: %s", payload.username)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )
