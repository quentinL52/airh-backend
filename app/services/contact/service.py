import resend
from app.config import settings
from app.schemas.contact_schemas import ContactForm

resend.api_key = settings.RESEND_API_KEY 

async def send_contact_email(form_data: ContactForm):
    receiver_email = settings.GMAIL_USER 
    sender_email = settings.SENDER_EMAIL
    
    subject = f"Nouveau message de contact : {form_data.name} ({form_data.email})"
    body = f"""
    Nom: {form_data.name}
    Email: {form_data.email}

    Message:
    {form_data.message}
    """

    params = {
      "from": f"AIrh Contact <{sender_email}>", 
      "to": [receiver_email],
      "subject": subject,
      "text": body,
    }

    try:
        email = resend.Emails.send(params)
        return {"message": "Email sent successfully via Resend", "resend_id": email.get("id")}
        
    except Exception as e:
        print(f"RESEND ERROR: {e}") 
        raise Exception(f"Failed to send email via Resend: {e}")