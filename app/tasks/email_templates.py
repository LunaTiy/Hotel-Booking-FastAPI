from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr
) -> EmailMessage:
    email_message = EmailMessage()

    email_message["Subject"] = "Подтверждение бронирования"
    email_message["From"] = settings.smtp_user
    email_message["To"] = email_to

    email_message.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )

    return email_message
