import requests
import os
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

#send_whatsapp_message("258860716912", "Hello World")