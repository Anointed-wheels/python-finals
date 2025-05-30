import random
from django.core.mail import send_mail
from django.utils import timezone

ALLOWED_TOKEN_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Custom set without confusing chars
TOKEN_LENGTH = 6

def generate_token():
    return ''.join(random.choices(ALLOWED_TOKEN_CHARS, k=TOKEN_LENGTH))

def send_token_email(email, token):
    send_mail(
        subject="",
        message=token,
        from_email="no-reply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )