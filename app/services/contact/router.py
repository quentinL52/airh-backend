from fastapi import APIRouter, HTTPException
from app.schemas.contact_schemas import ContactForm
from app.services.contact import service

router = APIRouter()

@router.post("", response_model=dict)
async def send_contact_form(form_data: ContactForm):
    try:
        await service.send_contact_email(form_data)
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))