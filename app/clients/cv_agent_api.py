import httpx
from fastapi import UploadFile
from app.config import settings

async def parse_cv(file_content: bytes, filename: str, content_type: str):
    async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
        files = {'file': (filename, file_content, content_type)}
        response = await client.post(
            f"{settings.CV_API_URL}/parse-cv/", 
            files=files
        )
        
        response.raise_for_status()
        return response.json()

async def simulate_interview(prompt: str):
    async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
        response = await client.post(f"{settings.CV_API_URL}/simulate", json={"prompt": prompt})
        response.raise_for_status()
        return response.json()