import os
from dotenv import load_dotenv
import fastapi.security as security
import boto3
from fastapi_mail import ConnectionConfig

load_dotenv('.env')

FRONTEND_URL = os.environ.get("FRONTEND_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_VERSION = os.environ.get("API_VERSION")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")
LOG_LEVEL = "debug"
JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
OAUTH2_SCHEME = security.OAuth2PasswordBearer(tokenUrl='/api/login')
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL")
JWT_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
JWT_TOKEN_EXPIRE_EMAIL_MINUTES = 15
ALGORITHM = "HS256"
AUTH_SCHEME = security.HTTPBearer()
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                         region_name=AWS_REGION_NAME)

S3_BUCKET_URL = os.environ.get("S3_BUCKET_URL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

EMAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=EMAIL_HOST_USER,
    MAIL_PASSWORD=EMAIL_HOST_PASSWORD,
    MAIL_FROM=EMAIL_HOST_USER,
    MAIL_PORT=EMAIL_PORT,
    MAIL_SERVER=EMAIL_HOST,
    MAIL_STARTTLS = EMAIL_USE_TLS,
    MAIL_SSL_TLS = EMAIL_USE_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)
WOLFRAM_ALPHA_APPID = os.environ.get("WOLFRAM_ALPHA_APPID")
AUTH_BACKEND_URL = os.environ.get("AUTH_BACKEND_URL")
MONGODB_ADMIN_USER = os.environ.get("MONGODB_ADMIN_USER")
MONGODB_ADMIN_PASS = os.environ.get("MONGODB_ADMIN_PASS")