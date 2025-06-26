import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()  # Load environment variables from .env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, 'core', 'serviceAccountKey.json')

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

FIREBASE_WEB_API_KEY = os.environ.get('FIREBASE_WEB_API_KEY')

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))

def send_email(to_email, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise Exception("EMAIL_ADDRESS and EMAIL_PASSWORD must be set in environment variables.")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")
