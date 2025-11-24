from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum, DateTime, Text, Date
from datetime import datetime, date
from typing import List, Optional
from enum import Enum as PyEnum
from passlib.hash import bcrypt


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'


class TypeChoices(str, PyEnum):
    luxury = 'luxury'
    semiluxury = 'semiluxury'
    economy = 'economy'
    family = 'family'
    single = 'single'


class StatusChoices(str, PyEnum):
    available = 'available'
    booked = 'booked'
    occupied = 'occupied'



class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_name: Mapped[str] = mapped_column(String(32), unique=True)
    user_country: Mapped[List['UserProfile']] = relationship(back_populates='country',
                                                            cascade='all, delete-orphan')
    country_hotels: Mapped[List['Hotel']] = relationship(back_populates='hotel_country',
                                                        cascade='all, delete-orphan')


class UserProfile(Base):
    __tablename__ = 'userprofile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country: Mapped[Country] = relationship(back_populates="user_country")
    last_name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    created_date: Mapped[datetime]= mapped_column(DateTime, default=datetime.utcnow)
    owner_hotels: Mapped[List['Hotel']] = relationship(back_populates='owner',
                                                        cascade='all, delete-orphan')
    user_booking: Mapped[List['Booking']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')
    user_review: Mapped[List['Review']] = relationship(back_populates='review_user',
                                                         cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship('RefreshToken',
                                                            back_populates='token_user',
                                                             cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.password = bcrypt.hash(password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())



class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city_name: Mapped[str] = mapped_column(String(32), unique=True)
    city_hotels: Mapped[List['Hotel']] = relationship(back_populates='city',
                                                      cascade='all, delete-orphan')



class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    service_name: Mapped[str] = mapped_column(String(32), unique=True)




class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(64))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(back_populates='city_hotels')
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    hotel_country: Mapped[Country] = relationship(Country, back_populates='country_hotels')
    hotel_stars: Mapped[int] = mapped_column(Integer)
    street: Mapped[str] = mapped_column(String(100))
    postal_index: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='owner_hotels')
    image_hotels: Mapped[List['HotelImage']] = relationship(back_populates='hotel',
                                                      cascade='all, delete-orphan')
    room_hotels: Mapped[List['Room']] = relationship(back_populates='room_hotel',
                                                     cascade='all, delete-orphan')
    booking_hotels: Mapped[List['Booking']] = relationship(back_populates='hotel_booking',
                                                           cascade='all, delete-orphan')
    review_hotels: Mapped[List['Review']] = relationship(back_populates='hotel_review',
                                                         cascade='all, delete-orphan')





class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='image_hotels')
    hotel_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)



class Room(Base):

    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_hotel: Mapped[Hotel] = relationship(Hotel, back_populates='room_hotels')
    room_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    type: Mapped[TypeChoices] = mapped_column(Enum(TypeChoices), default=TypeChoices.luxury)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.available)
    price: Mapped[int] = mapped_column(Integer)
    room_description: Mapped[str] = mapped_column(Text)
    room_image: Mapped[List['RoomImage']] = relationship(back_populates='room',
                                                     cascade='all, delete-orphan')
    booking_room: Mapped[List['Booking']] = relationship(back_populates='room_booking',
                                                         cascade='all, delete-orphan')


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(Room, back_populates='room_image')
    image_room: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_booking: Mapped[Hotel] = relationship(Hotel, back_populates='booking_hotels')
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room_booking: Mapped[Room] = relationship(Room, back_populates='booking_room')
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_booking')
    check_in: Mapped[date] = mapped_column(DateTime, default=datetime.utcnow)
    check_out: Mapped[date] = mapped_column(Date)



class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_review: Mapped[Hotel] = relationship(Hotel, back_populates='review_hotels')
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    review_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_review')
    comment: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
