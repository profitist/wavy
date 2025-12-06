import os

from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
S3_ID = os.getenv("S3_ID")
S3_SECRET = os.getenv("S3_SERVER")