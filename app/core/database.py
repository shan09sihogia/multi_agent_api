from pymongo import MongoClient
from app.core.config import MONGO_URI, DB_NAME


client = MongoClient(MONGO_URI)
db     = client[DB_NAME]


def get_mongo_db():
    client = MongoClient(MONGO_URI)
    try:
        yield client[DB_NAME]
    finally:
        client.close()
