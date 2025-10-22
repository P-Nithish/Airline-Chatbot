import os
from django.conf import settings
from pymongo import MongoClient, ASCENDING

_client = MongoClient(settings.MONGO_URL)
db = _client[settings.MONGO_DB]

# Collections
users = db["users"]

users.create_index([("username_lower", ASCENDING)], unique=True, name="uniq_username_lower")
users.create_index([("user_id", ASCENDING)], unique=True, name="uniq_user_id")

def ping():
    return db.command("ping")
