from fastapi import Depends, HTTPException, APIRouter ,status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import RoomImage
from hotel_app.db.schema import RoomImageCreateSchema, RoomImageOutSchema
from sqlalchemy.orm import Session
from typing import List


room_image_router = APIRouter(prefix='/room_image', tags=['RoomImage'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_image_router.post('/create', response_model=RoomImageOutSchema)
async def room_image_create(room_image: RoomImageCreateSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db


@room_image_router.get('/list', response_model=List[RoomImageOutSchema])
async def room_image_list(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()


@room_image_router.get('/detail',response_model=RoomImageOutSchema)
async def detail_room_image(room_image_id:int,db:Session=Depends(get_db)):
    room_image_db=db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if room_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return room_image_db


@room_image_router.put('/update',response_model=RoomImageOutSchema)
async def update_room_image(room_image_id:int,room_image_data:RoomImageCreateSchema,db:Session=Depends(get_db)):
    room_image_db=db.query(RoomImage).filter(RoomImage.id== room_image_id).first()
    if room_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for room_image_key,room_image_value in  room_image_data.dict().items():
        setattr(room_image_db,room_image_key,room_image_value)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db




@room_image_router.delete('/delete')
async def delete_room_image(room_image_id:int,db:Session=Depends(get_db)):
    room_image_db=db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if room_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(room_image_db)
    db.commit()
    return {'answer':'success deleted'}