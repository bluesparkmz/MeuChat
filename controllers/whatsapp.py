import requests
import os
import secrets
from datetime import datetime, timedelta

import models

url = "https://bluesparkmz-api-sap.up.railway.app/message/sendText/Skyvenda MZ"

def send_whatsapp_message(number: str, text: str):
    payload = {
        "number": number,
        "text": text,
        "delay": 0,
        "linkPreview": False,
    }

    headers = {
        "apikey": os.getenv("API_KEY_WHATSAPP"),
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


def generate_otp_code() -> str:
    # Comentario: codigo de 6 digitos.
    return f"{secrets.randbelow(1000000):06d}"


def create_password_reset_otp(db, user: models.User, ttl_minutes: int = 10) -> models.PasswordResetOTP:
    code = generate_otp_code()
    otp = models.PasswordResetOTP(
        user_id=user.id,
        phone=user.phone or "",
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes),
        used=False,
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp


def send_password_reset_otp(number: str, code: str):
    text = f"Seu codigo de recuperacao MeuChat e: {code}"
    return send_whatsapp_message(number, text)

#send_whatsapp_message("258860716912", "Hello World")
