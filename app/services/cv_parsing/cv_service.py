import httpx
from fastapi import UploadFile, HTTPException
from typing import Dict, Any, Optional
from app.config import settings
from datetime import datetime
import logging
from app.services.cv_parsing.cv_cache import get_cv_from_cache, set_cv_in_cache, clear_cv_cache

logger = logging.getLogger(__name__)

async def process_cv_upload(user_id: str, file: UploadFile) -> Dict[str, Any]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="PDF file required")
    
    file_content = await file.read()
    logger.info(f"Étape 1 : Lecture du fichier et appel de l'API de parsing du CV.")
    
    try:
        cv_parsing_url = f"{settings.CV_API_URL}/parse-cv/"
        files = {'file': (file.filename, file_content, file.content_type)}
        timeout = httpx.Timeout(None, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            logger.info(f"Appel de l'API de parsing: {cv_parsing_url}")
            response = await client.post(cv_parsing_url, files=files)
            response.raise_for_status()
            parsed_cv_data = response.json()
            logger.info("Parsing CV réussi")
            
    except httpx.TimeoutException:
        logger.error("Timeout lors de la lecture de la réponse de l'API de parsing du CV.")
        raise HTTPException(status_code=504, detail="Timeout lors de l'analyse du CV. Veuillez réessayer.")
    except httpx.HTTPStatusError as e:
        logger.error(f"Erreur HTTP de l'API de parsing: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Erreur de l'API de parsing de CV: {e.response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de l'appel de l'API de parsing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Échec de la communication avec l'API de parsing de CV: {str(e)}")

    try:
        logger.info("Étape 2 : Sauvegarde du CV dans la base de données.")
        data_access_url = f"{settings.DATA_ACCESS_API_URL}/api/v1/cvs"
        cv_payload = {
            "user_id": user_id,
            "parsed_data": parsed_cv_data,
            "upload_date": datetime.utcnow().isoformat()
        }
        
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            response = await client.post(data_access_url, json=cv_payload)
            response.raise_for_status()
            cv_db_entry = response.json()
            cv_id = cv_db_entry.get("_id")
            if not cv_id:
                raise ValueError("L'ID du document CV n'a pas été renvoyé par l'API de données.")
            logger.info(f"CV sauvegardé avec l'ID: {cv_id}")
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Erreur HTTP lors de la sauvegarde: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Erreur de l'API de données (stockage du CV): {e.response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Échec de la sauvegarde du CV dans la base de données: {str(e)}")
    
    try:
        logger.info("Étape 3 : Mise à jour du profil utilisateur.")
        user_update_url = f"{settings.DATA_ACCESS_API_URL}/api/v1/users/{user_id}"
        user_update_payload = {"candidate_mongo_id": cv_id}
        
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            response = await client.put(user_update_url, json=user_update_payload)
            response.raise_for_status()
            updated_user = response.json()
            logger.info("Profil utilisateur mis à jour avec succès")
            await clear_cv_cache(user_id)
            return updated_user
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Erreur HTTP lors de la mise à jour utilisateur: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Erreur de l'API de données (mise à jour de l'utilisateur): {e.response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour utilisateur: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Échec de la mise à jour du profil utilisateur: {str(e)}") 
    
async def get_user_cv_data(user_id: str) -> Optional[Dict[str, Any]]:
    try:
        cv_data_from_cache = await get_cv_from_cache(user_id)
        if cv_data_from_cache:
            logger.info(f"CV data retrieved from cache for user {user_id}")
            return cv_data_from_cache
        user_info_url = f"{settings.DATA_ACCESS_API_URL}/api/v1/users/{user_id}"
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            user_response = await client.get(user_info_url)
            user_response.raise_for_status()
            user_data = user_response.json()
            candidate_mongo_id = user_data.get("candidate_mongo_id")

        if not candidate_mongo_id:
            return None 

        cv_data_url = f"{settings.DATA_ACCESS_API_URL}/api/v1/cvs/{candidate_mongo_id}"
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            cv_response = await client.get(cv_data_url)
            cv_response.raise_for_status()
            cv_data = cv_response.json()
            await set_cv_in_cache(user_id, cv_data)
            return cv_data

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise HTTPException(status_code=e.response.status_code, detail=f"Erreur de l'API de données: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la récupération des données du CV: {str(e)}")