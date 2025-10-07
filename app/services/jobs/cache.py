import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.clients.job_offer_api import get_job_offers
from app.schemas.jobs_schemas import JobOffer

cached_job_offers: List[Dict[str, Any]] = []
last_update: datetime | None = None
cache_lock = asyncio.Lock()

async def update_job_offers_cache():
    """
    Tâche de fond pour récupérer les offres d'emploi et mettre à jour le cache.
    """
    global cached_job_offers, last_update
    print("Mise à jour du cache des offres d'emploi...")
    try:
        job_offers = await get_job_offers()
        validated_offers = [JobOffer(**offer).model_dump(by_alias=True) for offer in job_offers]
        validated_offers.sort(key=lambda x: datetime.strptime(x['publication'], "%d/%m/%Y"), reverse=True)
        
        async with cache_lock:
            cached_job_offers = validated_offers
            last_update = datetime.utcnow()
            print(f"Cache des offres d'emploi mis à jour. Nombre d'offres : {len(cached_job_offers)}")
            
    except Exception as e:
        print(f"Erreur lors de la mise à jour du cache : {e}")

def get_job_offers_from_cache() -> List[Dict[str, Any]]:
    """
    Récupère les offres d'emploi depuis le cache en mémoire.
    """
    return cached_job_offers