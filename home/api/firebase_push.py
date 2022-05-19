from asyncio.log import logger
import requests
from django.conf import settings

FIREBASE_SEND_URL = "https://fcm.googleapis.com/fcm/send"
def get_headers():
    return {
        "Authorization": f"key={settings.FIREBASE_API_KEY}",
        "Content-type": "application/json",
    }

def get_message_payload(token, message):
    return {
        "to": token,
        "data": {
            "title": "Yangi buyurtma",
            "body": message,
            },
    }

def send_notification(token, message):
    """Function that send_notification to the user's phone app,
    """
    try:

        payload = get_message_payload(token, message)
        headers = get_headers()
        r = requests.post(FIREBASE_SEND_URL, json=payload, headers=headers)
        if r.status_code == 200:
            logger.info(f"Notification sent {r.status_code}")
        else:
            logger.error(f"Notification not sent to {token} {r.status_code}")
        return r
    except Exception as e:
        logger.error(f"{e} Error while sending notification to {token}")
        return None


def run_send_notification(mobile_users):
    import django
    django.setup()
    for i in mobile_users:
            if i.firebase_token:
                send_notification(i.firebase_token, 'Yangi buyurtma yaratildi!')