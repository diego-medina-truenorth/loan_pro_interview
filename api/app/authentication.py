from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .model.orm import User
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_by_username(username: str):
    user = User(username="admin", password=pwd_context.hash("password"))
    return user


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def generate_access_token(user: User):
    token_data = {"user_id": user.id, "username": user.username}
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
