from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    # Project settings 
    PROJECT_NAME: str = "AI Interview API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT 
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Email 
    SENDER_EMAIL: str
    GMAIL_USER: str
    GMAIL_PASSWORD: str
    RESEND_API_KEY: str

    # MongoDB 
    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_CV_COLLECTION: str
    MONGO_INTERVIEW_COLLECTION: str
    MONGO_FEEDBACK_COLLECTION: str

    # PostgreSQL 
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    # External APIs 
    API_TIMEOUT: int = 80
    JOB_API_URL: str
    DATA_ACCESS_API_URL: str
    CV_API_URL: str

    # Google OAuth 
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/google/callback"

    # Frontend URLs 
    FRONTEND_URL: str = "http://localhost:5173"
    FRONTEND_SUCCESS_URL: str = "http://localhost:5173/auth/callback"
    FRONTEND_ERROR_URL: str = "http://localhost:5173/auth/callback"

    class Config:
        env_file = ".env"

load_dotenv()
settings = Settings()