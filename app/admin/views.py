import typing

from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list: typing.ClassVar = [User.id, User.email, User.bookings]
    column_details_exclude_list: typing.ClassVar = [User.hashed_password]
    can_delete = False

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class HotelAdmin(ModelView, model=Hotel):
    column_list = "__all__"

    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = "__all__"

    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"

    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"
