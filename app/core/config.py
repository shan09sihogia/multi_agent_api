import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI   = os.getenv("MONGO_URI")
DB_NAME     = os.getenv("DB_NAME")

REDIS_URL   = os.getenv("REDIS_URL")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
