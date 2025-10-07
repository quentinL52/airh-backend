from typing import Dict, Any, Optional
import asyncio

cached_cv_data: Dict[str, Dict[str, Any]] = {}
cache_lock = asyncio.Lock()

async def get_cv_from_cache(user_id: str) -> Optional[Dict[str, Any]]:
    async with cache_lock:
        return cached_cv_data.get(user_id)

async def set_cv_in_cache(user_id: str, cv_data: Dict[str, Any]):
    async with cache_lock:
        cached_cv_data[user_id] = cv_data

async def clear_cv_cache(user_id: str):
    async with cache_lock:
        if user_id in cached_cv_data:
            del cached_cv_data[user_id]