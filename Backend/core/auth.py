import bcrypt
from typing import Optional, Tuple
from .mongo import users
from .ids import next_customer_id

def _normalize_username(username: str) -> str:
    return username.strip().lower()

def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12))

def verify_password(plain: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed)

def create_user(username: str, password: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    uname_norm = _normalize_username(username)
    if users.find_one({"username_lower": uname_norm}):
        return False, None, "Username already exists"

    user_doc = {
        "user_id": next_customer_id(),                
        "username": username.strip(),
        "username_lower": uname_norm,
        "password_hash": hash_password(password),
    }
    users.insert_one(user_doc)
    return True, {"user_id": user_doc["user_id"], "username": user_doc["username"]}, None

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    uname_norm = _normalize_username(username)
    doc = users.find_one({"username_lower": uname_norm})
    if not doc or not verify_password(password, doc.get("password_hash", b"")):
        return False, None, "Invalid username or password"
    return True, {"user_id": doc["user_id"], "username": doc["username"]}, None
