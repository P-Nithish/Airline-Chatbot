import bcrypt
import uuid
from typing import Optional, Tuple
from .mongo import users

def _normalize_username(username: str) -> str:
    return username.strip().lower()

def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12))

def verify_password(plain: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except Exception:
        return False

def create_user(username: str, password: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    uname_norm = _normalize_username(username)
    # quick existence check
    if users.find_one({"username_lower": uname_norm}):
        return False, None, "Username already exists"

    user_doc = {
        "user_id": str(uuid.uuid4()),             
        "username": username.strip(),             
        "username_lower": uname_norm,             
        "password_hash": hash_password(password), 
    }
    users.insert_one(user_doc)
    return True, {"user_id": user_doc["user_id"], "username": user_doc["username"]}, None

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    uname_norm = _normalize_username(username)
    doc = users.find_one({"username_lower": uname_norm})
    if not doc:
        return False, None, "Invalid username or password"
    if not verify_password(password, doc.get("password_hash", b"")):
        return False, None, "Invalid username or password"
    return True, {"user_id": doc["user_id"], "username": doc["username"]}, None

def get_user_by_id(user_id: str) -> Optional[dict]:
    return users.find_one({"user_id": user_id}, {"_id": 0, "user_id": 1, "username": 1})
