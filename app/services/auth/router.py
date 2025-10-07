from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal 
from app.schemas.auth_schemas import Token, AuthResponse, TokenValidationRequest, TokenValidationResponse
from app.services.auth import service
from app.services.auth.oauth_service import oauth_service
from app.services.auth.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
import urllib.parse
import json
import traceback
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def get_db():
    async with SessionLocal() as session: 
        yield session

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    user = await service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/oauth/{provider}")
async def oauth_redirect(provider: str):
    if provider == "google":
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={urllib.parse.quote(settings.GOOGLE_REDIRECT_URI)}&"
            "scope=openid email profile&"
            "response_type=code&"
            "access_type=offline"
        )
        return RedirectResponse(google_auth_url)
    raise HTTPException(status_code=400, detail="Provider not supported")

@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: str, 
    code: str = None, 
    error: str = None,
    db: AsyncSession = Depends(get_db)
):
    if error:
        error_url = f"{settings.FRONTEND_ERROR_URL}?error={error}"
        return RedirectResponse(error_url)
    if not code:
        error_url = f"{settings.FRONTEND_ERROR_URL}?error=no_code"
        return RedirectResponse(error_url)
    try:
        auth_result = await oauth_service.authenticate_user(provider, code, db)
        
        def json_serializer(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            if hasattr(obj, 'hex'):
                return obj.hex
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        user_json_string = json.dumps(auth_result['user'], default=json_serializer)
        success_url = (
            f"{settings.FRONTEND_SUCCESS_URL}?"
            f"user={urllib.parse.quote(user_json_string)}"
        )
        response = RedirectResponse(url=success_url)
        response.set_cookie(
            key="access_token",
            value=auth_result['access_token'],
            httponly=True,
            samesite='lax',
            secure=False,  
            path="/",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        return response

    except Exception as e:
        tb_str = traceback.format_exc()
        logger.error(f"OAuth callback error: {e}\nFULL TRACEBACK:\n{tb_str}")
        error_url = f"{settings.FRONTEND_ERROR_URL}?error=auth_failed"
        return RedirectResponse(error_url)

@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await get_current_user(request, db) 
        return TokenValidationResponse(
            valid=True,
            user={
                "id": str(user.id),
                "email": user.email,
                "name": getattr(user, 'name', user.email.split('@')[0]),
                "picture_url": getattr(user, 'picture_url', None),
                "google_id": getattr(user, 'google_id', None),
                "candidate_mongo_id": getattr(user, 'candidate_mongo_id', None),
                "is_active": getattr(user, 'is_active', True),
                "created_at": user.created_at.isoformat() if getattr(user, 'created_at', None) else None
            }
        )
    except Exception as e:
        return TokenValidationResponse(valid=False, user=None)