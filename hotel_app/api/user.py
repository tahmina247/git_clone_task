from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import UserProfile
from hotel_app.db.schema import UserprofileCreateSchema, UserprofileOutSchema
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix='/user', tags=['UserProfile'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get('/list', response_model=List[UserprofileOutSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/detail', response_model=UserprofileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Myndady adam tabylgan jok')
    return user_db



@user_router.put('/update', response_model=UserprofileOutSchema)
async def update_user(user_id, user_data: UserprofileCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    for user_key, user_value in user_data.dict().items():
        setattr(user_db, user_key, user_value)
    db.commit()
    db.refresh(user_db)
    return user_db




@user_router.delete('/delete')
async def delete_user(user_id, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday maalymat jok')
    db.delete(user_db)
    db.commit()
    return {'answer db': 'success deleted'}