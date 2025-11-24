from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Room
from hotel_app.db.schema import RoomCreateSchema, RoomOutSchema
from sqlalchemy.orm import Session
from typing import List


room_router = APIRouter(prefix='/room', tags=['Room'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_router.post('/create', response_model=RoomOutSchema)
async def room_create(room: RoomCreateSchema, db: Session = Depends(get_db)):
    room_db = Room(**room.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db




@room_router.get('/list', response_model=List[RoomOutSchema])
async def room_list(db: Session = Depends(get_db)):
    return db.query(Room).all()


@room_router.get('/detail',response_model=RoomOutSchema)
async def detail_room(room_id:int,db:Session=Depends(get_db)):
    room_db=db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return room_db


@room_router.put('/update',response_model=RoomOutSchema)
async def update_room(room_id:int,room_data:RoomCreateSchema,db:Session=Depends(get_db)):
    room_db=db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for room_key, room_value in room_data.dict().items():
        setattr(room_db, room_key, room_value)
    db.commit()
    db.refresh(room_db)
    return room_db




@room_router.delete('/delete')
async def delete_room(room_id:int,db:Session=Depends(get_db)):
    room_db=db.query(Room).filter(Room.id == room_id).first()
    if room_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(room_db)
    db.commit()
    return {'answer':'success deleted'}