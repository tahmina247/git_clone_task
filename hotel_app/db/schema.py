from pydantic import BaseModel
from typing import Optional
from .models import RoleChoices, StatusChoices, TypeChoices
from datetime import datetime, date


class CountryCreateSchema(BaseModel):
    country_image: Optional[str]
    country_name: str


class CountryOutSchema(BaseModel):
    id: int
    country_image: Optional[str]
    country_name: str


class UserprofileCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    country_id: int
    email: str
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    role: RoleChoices
    created_date: datetime

    class Config:
        from_attributes = True



class UserprofileOutSchema(BaseModel):
    id: int
    country_id: int
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    role: RoleChoices
    created_date: datetime


    class Config:
        from_attributes = True


class UserProfileLoginShema(BaseModel):
    username: str
    password: str


    class Config:
        from_attributes = True



class CityCreateSchema(BaseModel):
    city_image: Optional[str]
    city_name: str



class CityOutSchema(BaseModel):
    id:int
    city_image: Optional[str]
    city_name: str



class ServiceCreateSchema(BaseModel):
    service_image: Optional[str]
    service_name: str


class ServiceOutSchema(BaseModel):
    id:int
    service_image: Optional[str]
    service_name: str



class HotelCreateSchema(BaseModel):
    hotel_name: str
    city_id: int
    country_id: int
    hotel_stars: int
    street: str
    postal_index: int
    description: str
    owner_id: int



class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    city_id: int
    country_id: int
    hotel_stars: int
    street: str
    postal_index: int
    description: str
    owner_id: int


class HotelImageCreateSchema(BaseModel):
    hotel_image: str
    hotel_id: int


class HotelImageOutSchema(BaseModel):
    id: int
    hotel_image: str
    hotel_id: int



class RoomCreateSchema(BaseModel):
    hotel_id: int
    room_number: int
    status: StatusChoices
    price: int
    room_description: str



class RoomOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_number: int
    status: StatusChoices
    price: int
    room_description: str
    type: TypeChoices



class RoomImageCreateSchema(BaseModel):
    room_id: int
    image_room: str


class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    image_room: str


class BookingCreateSchema(BaseModel):
    hotel_id: int
    room_id: int
    user_id: int
    check_in: date
    check_out: date



class BookingOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_id: int
    user_id: int
    check_in: date
    check_out: date



class ReviewCreateSchema(BaseModel):
    hotel_id: int
    user_id: int
    comment: str
    stars: int


class ReviewOutSchema(BaseModel):
    id: int
    hotel_id: int
    user_id: int
    comment: str
    stars: int

