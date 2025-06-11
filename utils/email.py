import random
from django.core.mail import send_mail
from django.utils import timezone

ALLOWED_TOKEN_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
TOKEN_LENGTH = 6

def generate_token():
    return ''.join(random.choices(ALLOWED_TOKEN_CHARS, k=TOKEN_LENGTH))

def send_token_email(email, token):
    send_mail(
        subject="Your confirmation code",
        message=token,
        from_email="no-reply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )

def send_activation(email, firstname):
    send_mail(
        subject="Account Approved",
        message=f"Dear {user.firstname}, Your account has been approved by the admin. You can now log in. Thank you.",
        from_email="no-reply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )