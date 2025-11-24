from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import HotelImage
from hotel_app.db.schema import HotelImageCreateSchema, HotelImageOutSchema
from sqlalchemy.orm import Session
from typing import List


hotel_image_router = APIRouter(prefix='/hotel_image', tags=['HotelImage'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_image_router.post('/create', response_model=HotelImageOutSchema)
async def hotel_image_create(hotel_image: HotelImageCreateSchema, db: Session = Depends(get_db)):
    hotel_image_db = HotelImage(**hotel_image.dict())
    db.add(hotel_image_db)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db




@hotel_image_router.get('/list', response_model=List[HotelImageOutSchema])
async def hotel_image_list(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()


@hotel_image_router.get('/detail',response_model=HotelImageOutSchema)
async def detail_hotel_image(hotel_image_id:int,db:Session=Depends(get_db)):
    hotel_image_db=db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if hotel_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return hotel_image_db


@hotel_image_router.put('/update',response_model=HotelImageOutSchema)
async def update_hotel_image(hotel_image_id:int,hotel_image_data:HotelImageCreateSchema,db:Session=Depends(get_db)):
    hotel_image_db=db.query(HotelImage).filter(HotelImage.id== hotel_image_id).first()
    if hotel_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for hotel_image_key,hotel_image_value in  hotel_image_data.dict().items():
        setattr(hotel_image_db,hotel_image_key,hotel_image_value)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db




@hotel_image_router.delete('/delete')
async def delete_hotel_image(hotel_image_id:int,db:Session=Depends(get_db)):
    hotel_image_db=db.query(HotelImage).filter(HotelImage.id==hotel_image_id).first()
    if hotel_image_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(hotel_image_db)
    db.commit()
    return {'answer':'success deleted'}