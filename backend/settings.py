import os
from dotenv import load_dotenv
import boto3
load_dotenv('.env')

FRONTEND_URL = os.environ.get("FRONTEND_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_VERSION = os.environ.get("API_VERSION")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")
LOG_LEVEL = "debug"
JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, 
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                         region_name=AWS_REGION_NAME)
rek_client = boto3.client("rekognition", 
                          aws_access_key_id=AWS_ACCESS_KEY_ID, 
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                          region_name=AWS_REGION_NAME)
S3_BUCKET_URL = os.environ.get("S3_BUCKET_URL")
WOLFRAM_ALPHA_APPID = os.environ.get("WOLFRAM_ALPHA_APPID")
AUTH_BACKEND_URL = os.environ.get("AUTH_BACKEND_URL")
MONGODB_ADMIN_USER = os.environ.get("MONGODB_ADMIN_USER")
MONGODB_ADMIN_PASS = os.environ.get("MONGODB_ADMIN_PASS")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
IMAGE_TO_TEXT = "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")