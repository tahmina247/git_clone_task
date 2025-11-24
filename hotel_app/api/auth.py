from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import UserProfile, RefreshToken
from hotel_app.db.schema import UserprofileCreateSchema, UserProfileLoginShema
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from hotel_app.config import (ALGORITHM, SECRET_KEY,
                              ACCESS_TOKEN_LIFETIME,
                              REFRESH_ACCESS_TOKEN_LIFETIME)
from datetime import timedelta, datetime



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def verify_password(plain_password, hashed_password): #(admin, fgfdgfdgfdgdfgfd)
    return pwd_context.verify(plain_password, hashed_password) #fgfdgfdgfdgdfgfd  == fgfdgfdgfdgdfgfd



def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_ACCESS_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user: UserprofileCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    user_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail='username бар экен')
    elif user_email:
        raise HTTPException(status_code=400, detail='email бар экен')
    hash_password = get_password_hash(user.password) #admin
    #hash_password = fgfdgfdgfdgdfgfd
    user_db = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        country_id=user.country_id,
        email=user.email,
        password=hash_password,
        age=user.age,
        phone_number=user.phone_number,
        role=user.role,
        created_date=user.created_date,
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {"message": 'Registered'}



@auth_router.post('/login')
async def login(form_data: UserProfileLoginShema, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Маалымат туура эмес")


    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    new_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(new_token)
    db.commit()


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):

    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымыт туура эмес")

    db.delete(stored_token)
    db.commit()

    return {"message": "Вышли"}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail="Маалымыт туура эмес")


    access_token = create_access_token({"sub": stored_token.id})

    return {"access_token": access_token, "token_type": "bearer"}








