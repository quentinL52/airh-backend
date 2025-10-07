from fastapi import APIRouter
from app.schemas.jobs_schemas import JobOffer
from app.services.jobs.cache import get_job_offers_from_cache

router = APIRouter()

@router.get("/", response_model=list[JobOffer])
async def get_all_job_offers():
    """
    Retrieve all job offers from the cache.
    """
    job_offers = get_job_offers_from_cache()
    if not job_offers:
        return []
    return job_offers