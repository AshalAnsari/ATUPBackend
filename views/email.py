import smtplib
from email.message import EmailMessage
from fastapi import Request
from itsdangerous import URLSafeTimedSerializer
from decouple import config

# Setup configurations
SECRET_KEY = config("SECRET_KEY")
EMAIL_USER = config("EMAIL_USER")
EMAIL_PASS = config("EMAIL_PASS")
BASE_URL = "http://localhost:8000"  # Update this for production

serializer = URLSafeTimedSerializer(SECRET_KEY)

def send_verification_email(user_email: str, user_id: str):
    token = user_id  # Replace with actual token logic if needed
    verify_url = f"{BASE_URL}/users/verify-email?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email - TalkBridge"
    msg["From"] = EMAIL_USER
    msg["To"] = user_email

    msg.set_content("Please use an HTML-compatible email client to view this message.")

    msg.add_alternative(f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
          <h2 style="color: #333;">Welcome to ATUP!</h2>
          <p style="color: #555;">Hi there,</p>
          <p style="color: #555;">Thank you for signing up. Please click the button below to verify your email address:</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{verify_url}" style="padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; font-weight: bold; border-radius: 5px;">Verify Email</a>
          </div>
          <p style="color: #999;">If you didn’t request this, you can safely ignore this email.</p>
          <p style="color: #999;">- The ATUP Team</p>
        </div>
      </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
