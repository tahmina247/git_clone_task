from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Hotel
from hotel_app.db.schema import HotelCreateSchema, HotelOutSchema
from sqlalchemy.orm import Session
from typing import List


hotel_router = APIRouter(prefix='/hotel', tags=['Hotel'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_router.post('/create', response_model=HotelOutSchema)
async def hotel_create(hotel: HotelCreateSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db




@hotel_router.get('/list', response_model=List[HotelOutSchema])
async def hotel_list(db: Session = Depends(get_db)):
    return db.query(Hotel).all()


@hotel_router.get('/detail',response_model=HotelOutSchema)
async def detail_hotel(hotel_id:int,db:Session=Depends(get_db)):
    hotel_db=db.query(Hotel).filter(Hotel.id ==hotel_id).first()
    if hotel_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return hotel_db


@hotel_router.put('/update',response_model=HotelOutSchema)
async def update_hotel(hotel_id:int,hotel_data:HotelCreateSchema,db:Session=Depends(get_db)):
    hotel_db=db.query(Hotel).filter(Hotel.id==hotel_id).first()
    if hotel_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for hotel_key,hotel_value in hotel_data.dict().items():
        setattr(hotel_db,hotel_key,hotel_value)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db




@hotel_router.delete('/delete')
async def delete_hotel(hotel_id:int,db:Session=Depends(get_db)):
    hotel_db=db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(hotel_db)
    db.commit()
    return {'answer':'success deleted'}