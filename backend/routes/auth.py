from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from services import auth_service
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=auth_service.User)
async def signup(user: auth_service.UserCreate):
    print(f"Signup request: {user}")
    if user.username in auth_service.users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth_service.get_password_hash(user.password)
    auth_service.users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    print(f"Updated users_db: {auth_service.users_db}")
    
    return auth_service.User(username=user.username, email=user.email)

@router.post("/login", response_model=auth_service.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login request: username={form_data.username}")
    user = auth_service.authenticate_user(auth_service.users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=auth_service.User)
async def read_users_me(current_user: auth_service.User = Depends(auth_service.get_current_user)):
    return current_user