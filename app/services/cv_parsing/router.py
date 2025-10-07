from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.services.cv_parsing import cv_service
from app.services.auth.security import get_current_user
from app.models.postgres.user_model import User
from app.schemas.interview_schemas import CVParseResponse

router = APIRouter()

@router.post("/cv", tags=["cv_parsing"])
async def upload_cv_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        user_id_str = str(current_user.id)
        result = await cv_service.process_cv_upload(user_id=user_id_str, file=file)
        return {"message": "CV uploaded, parsed, and linked successfully", "user_profile": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=CVParseResponse, tags=["cv_parsing"])
async def get_user_cv_by_id_endpoint(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à accéder à ce CV.")
        
    cv_data = await cv_service.get_user_cv_data(user_id)
    if not cv_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found for this user"
        )
    
    # MODIFICATION : Crée explicitement l'objet de réponse
    return CVParseResponse(
        cv_id=str(cv_data.get("_id")),
        parsed_data=cv_data.get("parsed_data")
    )
