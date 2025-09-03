import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/landflip")
API_CORS_ORIGINS = os.getenv("API_CORS_ORIGINS", "*").split(",")
