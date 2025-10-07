import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.schemas.contact_schemas import ContactForm

async def send_contact_email(form_data: ContactForm):
    sender_email = settings.GMAIL_USER
    sender_password = settings.GMAIL_PASSWORD
    receiver_email = settings.GMAIL_USER

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Contact Form: {form_data.subject} from {form_data.email}"

    body = f"Name: {form_data.name}\nEmail: {form_data.email}\n\nMessage:\n{form_data.message}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")
