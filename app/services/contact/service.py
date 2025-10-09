import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.schemas.contact_schemas import ContactForm
import Resend
resend_client = Resend(api_key=settings.RESEND_API_KEY)

async def send_contact_email(form_data: ContactForm):
    sender_email = settings.GMAIL_USER
    sender_password = settings.GMAIL_PASSWORD
    receiver_email = settings.GMAIL_USER

    subject = f"Nouveau message de contact : {form_data.name} ({form_data.email})"
    body = f"""
    Nom: {form_data.name}
    Email: {form_data.email}

    Message:
    {form_data.message}
    """

    try:
        resend_client.emails.send({
            "from": sender_email,
            "to": receiver_email,
            "subject": subject,
            "text": body,
        })
        return {"message": "Email sent successfully via Resend"}
        
    except Exception as e:
        raise Exception(f"Failed to send email via Resend: {e}")