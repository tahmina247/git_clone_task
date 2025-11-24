from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Booking
from hotel_app.db.schema import BookingCreateSchema, BookingOutSchema
from sqlalchemy.orm import Session
from typing import List


booking_router = APIRouter(prefix='/booking', tags=['Booking'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.post('/create', response_model=BookingOutSchema)
async def booking_create(booking: BookingCreateSchema, db: Session = Depends(get_db)):
    booking_db = Booking(**booking.dict())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db




@booking_router.get('/list', response_model=List[BookingOutSchema])
async def booking_list(db: Session = Depends(get_db)):
    return db.query(Booking).all()



@booking_router.get('/detail',response_model=BookingOutSchema)
async def detail_booking(booking_id:int,db:Session=Depends(get_db)):
    booking_db=db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return booking_db


@booking_router.put('/update',response_model=BookingOutSchema)
async def update_booking(booking_id:int,booking_data:BookingCreateSchema,db:Session=Depends(get_db)):
    booking_db=db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for booking_key, booking_value in  booking_data.dict().items():
        setattr(booking_db, booking_key, booking_value)
    db.commit()
    db.refresh(booking_db)
    return booking_db




@booking_router.delete('/delete')
async def delete_booking(booking_id:int,db:Session=Depends(get_db)):
    booking_db=db.query(Booking).filter(Booking.id==booking_id).first()
    if booking_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(booking_db)
    db.commit()
    return {'answer':'success deleted'}