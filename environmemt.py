import os

from dotenv import load_dotenv

load_dotenv()

# ==== app settings ====
WEB_URL = 'https://formrrito.fun'

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"
ALLOWED_HOSTS = [
    "127.0.0.1",
    ".localhost"
]

ACCESS_TOKEN_EXPIRE_MINUTES = 720

# ==== email service ====
EMAIL_HOST = os.getenv('EMAIL_HOST')
SERVICE_EMAIL = os.getenv('SERVICE_EMAIL')
SERVICE_EMAIL_PASSWORD = os.getenv('SERVICE_EMAIL_PASSWORD')
