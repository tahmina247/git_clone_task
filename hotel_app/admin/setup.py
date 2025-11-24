from fastapi import FastAPI
from sqladmin import Admin

from hotel_app.db.database import engine

from .views import (
    CountryAdmin, UserProfileAdmin, RefreshTokenAdmin,
    CityAdmin, ServiceAdmin, HotelAdmin, HotelImageAdmin,
    RoomAdmin, RoomImageAdmin, BookingAdmin, ReviewAdmin
)


def setup_admin(hotel_app: FastAPI):
    admin = Admin(hotel_app, engine)

    admin.add_view(UserProfileAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(HotelImageAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(RoomImageAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(ReviewAdmin)
