import httpx
from app.config import settings

async def get_job_offers():
    async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
        response = await client.get(settings.JOB_API_URL)
        response.raise_for_status()
        return response.json()
