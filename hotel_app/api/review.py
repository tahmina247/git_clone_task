from fastapi import Depends, HTTPException, APIRouter, status
from hotel_app.db.database import SessionLocal
from hotel_app.db.models import Review
from hotel_app.db.schema import ReviewCreateSchema, ReviewOutSchema
from sqlalchemy.orm import Session
from typing import List


review_router = APIRouter(prefix='/review', tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/create', response_model=ReviewOutSchema)
async def review_create(review: ReviewCreateSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db




@review_router.get('/list', response_model=List[ReviewOutSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/detail',response_model=ReviewOutSchema)
async def detail_review(review_id:int,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    return review_db


@review_router.put('/update',response_model=ReviewOutSchema)
async def update_review(review_id:int,review_data:ReviewCreateSchema,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    for review_key, review_value in  review_data.dict().items():
        setattr(review_db, review_key, review_value)
    db.commit()
    db.refresh(review_db)
    return review_db




@review_router.delete('/delete')
async def delete_review(review_id:int,db:Session=Depends(get_db)):
    review_db=db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='mynday maalymat jok')
    db.delete(review_db)
    db.commit()
    return {'answer':'success deleted'}