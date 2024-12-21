from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = f"https://www.legalizeme.site/password-reset/?token={reset_password_token.key}"
    subject = "Password Reset Request"
    body = f"""
    Dear User,

    You requested to reset your password. Please click the link below to reset your password:
    {reset_url}

    If you did not request this change, please ignore this email.

    Best regards,
    Legalize Me Team
    """
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = reset_password_token.user.email

    try:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            print("Password reset email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")