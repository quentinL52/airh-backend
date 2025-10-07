# app/main.py
import asyncio
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.auth.router import router as auth_router
from app.services.contact.router import router as contact_router
from app.services.jobs.router import router as jobs_router
from app.services.jobs.cache import update_job_offers_cache
from app.services.cv_parsing.router import router as cv_parsing_router
from app.config import settings

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await update_job_offers_cache()
    scheduler.add_job(update_job_offers_cache, 'interval', minutes=60)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False,
    lifespan=lifespan
)

origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://localhost:8080",
    #"http://localhost:5173", 
    "https://www.airh.online", 
    settings.FRONTEND_SUCCESS_URL.split('/auth')[0],
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(contact_router, prefix=f"{settings.API_V1_STR}/contact", tags=["Contact"])
app.include_router(jobs_router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Jobs"])
app.include_router(cv_parsing_router, prefix=f"{settings.API_V1_STR}/cv_parsing", tags=["cv_parsing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Interview API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}