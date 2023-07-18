from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .model.orm import User
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
