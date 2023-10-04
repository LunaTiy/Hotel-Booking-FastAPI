from sqladmin import ModelView

from app.bookings.models import Booking
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"

    name = "Бронирование"
    name_plural = "Бронирования"
