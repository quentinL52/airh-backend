from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    picture_url: str | None = None
    google_id: str | None = None
    candidate_mongo_id: str | None = None
    is_active: bool = True
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenValidationRequest(BaseModel):
    token: str

class TokenValidationResponse(BaseModel):
    valid: bool
    user: UserResponse | None = None