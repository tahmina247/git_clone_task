from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import City
from hotel_app.db.schema import CityCreateSchema, CityOutSchema
from sqlalchemy.orm import Session
from typing import List


city_router = APIRouter(prefix='/city', tags=['City'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post('/create', response_model=CityOutSchema)
async def city_create(city: CityCreateSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db



@city_router.get('/list', response_model=List[CityOutSchema])
async def city_list(db: Session = Depends(get_db)):
    return db.query(City).all()



@city_router.get('/detail',response_model=CityOutSchema)
async def detail_city(city_id:int,db:Session=Depends(get_db)):
    city_db=db.query(City).filter(City.id ==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return city_db


@city_router.put('/update',response_model=CityOutSchema)
async def update_city(city_id:int,city_data:CityCreateSchema,db:Session=Depends(get_db)):
    city_db=db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for city_key,city_value in city_data.dict().items():
        setattr(city_db,city_key,city_value)
    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.delete('/delete')
async def delete_city(city_id:int,db:Session=Depends(get_db)):
    city_db=db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(city_db)
    db.commit()
    return {'answer':'success deleted'}

