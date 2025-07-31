import smtplib
from email.message import EmailMessage
from fastapi import Request
from itsdangerous import URLSafeTimedSerializer
from decouple import config  # Or use os.environ

# Setup the serializer
SECRET_KEY = config("SECRET_KEY")  # Set this in your .env file
EMAIL_USER = config("EMAIL_USER")
EMAIL_PASS = config("EMAIL_PASS")
BASE_URL = "http://localhost:8000"  # Change this to your frontend/backend base URL

serializer = URLSafeTimedSerializer(SECRET_KEY)

def send_verification_email(user_email: str, user_id: str):
    token = user_id
    verify_url = f"{BASE_URL}/users/verify-email?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = EMAIL_USER
    msg["To"] = user_email
    msg.set_content(f"""
    Hi there,\n

    Please click the button below to verify your email:\n\n

    <a href="{verify_url}" style="padding:10px 20px; background-color:#4CAF50; color:white; text-decoration:none;">
    Verify Email</a>\n\n

    If you did not request this, ignore this email.
    """, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
