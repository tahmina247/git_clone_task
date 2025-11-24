from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Country
from hotel_app.db.schema import CountryCreateSchema, CountryOutSchema
from sqlalchemy.orm import Session
from typing import List


country_router = APIRouter(prefix='/country', tags=['Country'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@country_router.post('/create', response_model=CountryOutSchema)
async def country_create(country: CountryCreateSchema, db: Session = Depends(get_db)):
    country_db = Country(**country.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db




@country_router.get('/list', response_model=List[CountryOutSchema])
async def country_list(db: Session = Depends(get_db)):
    return db.query(Country).all()



@country_router.get('/detail',response_model=CountryOutSchema)
async def detail_country(country_id:int,db:Session=Depends(get_db)):
    country_db=db.query(Country).filter(Country.id ==country_id).first()
    if country_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return country_db


@country_router.put('/update',response_model=CountryOutSchema)
async def update_country(country_id:int,country_data:CountryCreateSchema,db:Session=Depends(get_db)):
    country_db=db.query(Country).filter(Country.id==country_id).first()
    if country_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for country_key,country_value in country_data.dict().items():
        setattr(country_db,country_key,country_value)
    db.commit()
    db.refresh(country_db)
    return country_db




@country_router.delete('/delete')
async def delete_country(country_id:int,db:Session=Depends(get_db)):
    country_db=db.query(Country).filter(Country.id==country_id).first()
    if country_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(country_db)
    db.commit()
    return {'answer':'success deleted'}