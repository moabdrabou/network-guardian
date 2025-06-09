import requests
import smtplib
from email.mime.text import MIMEText
from config import (
    ENABLE_PUSHOVER, PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN,
    # ENABLE_EMAIL, EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD,
    # EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT
)

def send_notification(message):
    """Sends a notification using enabled methods."""
    print(f"Notification: {message}") # Always print to console

    if ENABLE_PUSHOVER:
        send_pushover_notification(message)

    # if ENABLE_EMAIL:
    #     send_email_notification(message)

def send_pushover_notification(message):
    """Sends a notification via Pushover."""
    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        print("Pushover credentials not set in config.py. Skipping Pushover notification.")
        return

    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": "Network Intruder Alert!",
        "priority": 1 # High priority
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print("Pushover notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Pushover notification: {e}")

# def send_email_notification(message):
#     """Sends a notification via Email."""
#     if not (EMAIL_SENDER and EMAIL_RECEIVER and EMAIL_PASSWORD and EMAIL_SMTP_SERVER):
#         print("Email credentials not fully set in config.py. Skipping email notification.")
#         return

#     msg = MIMEText(message)
#     msg['Subject'] = 'Network Intruder Alert!'
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = EMAIL_RECEIVER

#     try:
#         with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
#             server.starttls() # Secure the connection
#             server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
#         print("Email notification sent successfully.")
#     except Exception as e:
#         print(f"Error sending email notification: {e}")