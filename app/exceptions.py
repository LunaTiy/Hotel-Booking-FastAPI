﻿from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже зарегистрирован"


class IncorrectEmailOrPassword(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCantBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class CantRemoveBooking(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Невозможно удалить данное бронирование"


class IncorrectDataFormat(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный диапазон дат"


class IncorrectDataFormatDiapason(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Диапазон дат не должен превышать 30 дней"
