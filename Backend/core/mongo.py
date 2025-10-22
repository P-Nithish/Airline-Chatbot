from django.conf import settings
from pymongo import MongoClient, ASCENDING

_client = MongoClient(settings.MONGO_URL)
db = _client[settings.MONGO_DB]

users   = db["users"]
tickets = db["tickets"]
counters= db["counters"]

# user indexes (as before)
users.create_index([("username_lower", ASCENDING)], unique=True, name="uniq_username_lower")
users.create_index([("user_id", ASCENDING)],        unique=True, name="uniq_user_id")

# tickets indexes – match your schema
tickets.create_index([("user_id", ASCENDING)], name="idx_tickets_user")
tickets.create_index([("Seat_status", ASCENDING)], name="idx_tickets_Seat_status")
tickets.create_index([("flight_id", ASCENDING), ("seat_no", ASCENDING)], name="idx_flight_seat")
