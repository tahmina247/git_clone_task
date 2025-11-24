from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Service
from hotel_app.db.schema import ServiceCreateSchema, ServiceOutSchema
from sqlalchemy.orm import Session
from typing import List


service_router = APIRouter(prefix='/service', tags=['Service'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@service_router.post('/create', response_model=ServiceOutSchema)
async def service_create(service: ServiceCreateSchema, db: Session = Depends(get_db)):
    service_db = Service(**service.dict())
    db.add(service_db)
    db.commit()
    db.refresh(service_db)
    return service_db




@service_router.get('/list', response_model=List[ServiceOutSchema])
async def service_list(db: Session = Depends(get_db)):
    return db.query(Service).all()



@service_router.get('/detail',response_model=ServiceOutSchema)
async def detail_service(service_id:int,db:Session=Depends(get_db)):
    service_db=db.query(Service).filter(Service.id ==service_id).first()
    if service_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return service_db


@service_router.put('/update',response_model=ServiceOutSchema)
async def update_service(service_id:int,service_data:ServiceCreateSchema,db:Session=Depends(get_db)):
    service_db=db.query(Service).filter(Service.id==service_id).first()
    if service_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for service_key,service_value in  service_data.dict().items():
        setattr(service_db,service_key,service_value)
    db.commit()
    db.refresh(service_db)
    return service_db




@service_router.delete('/delete')
async def delete_service(service_id:int,db:Session=Depends(get_db)):
    service_db=db.query(Service).filter(Service.id==service_id).first()
    if service_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(service_db)
    db.commit()
    return {'answer':'success deleted'}