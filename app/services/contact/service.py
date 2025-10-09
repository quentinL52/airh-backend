import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.schemas.contact_schemas import ContactForm
import resend
resend = resend(api_key=settings.RESEND_API_KEY)

async def send_contact_email(form_data: ContactForm):
    sender_email = settings.GMAIL_USER
    sender_password = settings.GMAIL_PASSWORD
    receiver_email = settings.GMAIL_USER

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
        # Utilisation de l'API Resend
        resend.emails.send({
            "from": sender_email,
            "to": receiver_email,
            "subject": subject,
            "text": body,
        })
        
        # Le code d'origine renvoyait un dictionnaire, 
        # mais la fonction est asynchrone et le router n'attend pas de retour spécifique, 
        # on peut donc juste retourner un message de succès (ou rien).
        return {"message": "Email sent successfully via Resend"}
        
    except Exception as e:
        # Il est important de bien typer l'exception, mais on garde la levée générale pour l'instant
        # Le router dans router.py va attraper cette exception et renvoyer un 500
        raise Exception(f"Failed to send email via Resend: {e}")