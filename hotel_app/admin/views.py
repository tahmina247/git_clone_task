from sqladmin import ModelView
from hotel_app.db.models import (
    Country, UserProfile, RefreshToken,
    City, Service, Hotel, HotelImage,
    Room, RoomImage, Booking, Review
)

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id,
        UserProfile.first_name,
        UserProfile.last_name,
    ]




class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [
        RefreshToken.id,
        RefreshToken.user_id,
        RefreshToken.token,
        RefreshToken.created_date
    ]


class CountryAdmin(ModelView, model=Country):
    column_list = [
        Country.id,
        Country.country_name,
    ]


class CityAdmin(ModelView, model=City):
    column_list = [
        City.id,
        City.city_name,
    ]


class ServiceAdmin(ModelView, model=Service):
    column_list = [
        Service.id,
        Service.service_name,
    ]


class HotelAdmin(ModelView, model=Hotel):
    column_list = [
        Hotel.id,
        Hotel.hotel_name,
    ]


class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = [
        HotelImage.id,
        HotelImage.hotel_image
    ]


class RoomAdmin(ModelView, model=Room):
    column_list = [
        Room.id,
        Room.room_number,
    ]


class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [
        RoomImage.id,
        RoomImage.room_id,
        RoomImage.image_room
    ]


class BookingAdmin(ModelView, model=Booking):
    column_list = [
        Booking.id,
        Booking.user_id,
        Booking.hotel_id,
        Booking.room_id,
        Booking.check_in,
        Booking.check_out
    ]


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.user_id,
        Review.hotel_id,
        Review.stars,

    ]
