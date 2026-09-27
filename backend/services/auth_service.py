from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import hashlib
import jwt
import os
from datetime import datetime, timedelta
from config import Config

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Secret key for JWT token generation (in production, use a more secure method)
SECRET_KEY = os.getenv("SECRET_KEY", "lawmind_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory user storage (in production, use a database)
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": hashlib.sha256("admin123".encode()).hexdigest(),
        "email": "admin@lawmind.com"
    }
}

print(f"Initial users_db: {users_db}")

class User(BaseModel):
    username: str
    email: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    result = hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    print(f"Verifying password: {plain_password} -> {hashlib.sha256(plain_password.encode()).hexdigest()} == {hashed_password} = {result}")
    return result

def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(db, username: str):
    print(f"Getting user: {username}")
    print(f"Current users_db: {db}")
    if username in db:
        user_dict = db[username]
        print(f"Found user: {user_dict}")
        return UserInDB(**user_dict)
    print(f"User {username} not found")
    return None

def authenticate_user(db, username: str, password: str):
    print(f"Authenticating user: {username}")
    user = get_user(db, username)
    if not user:
        print(f"User {username} not found")
        return False
    if not verify_password(password, user.hashed_password):
        print(f"Password verification failed for user {username}")
        return False
    print(f"Authentication successful for user {username}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user