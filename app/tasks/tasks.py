import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_setup import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_picture(
        path: str,
) -> None:
    image_path = Path(path)
    image = Image.open(image_path)

    image_resized = image.resize((1000, 500))
    image_preview = image.resize((200, 100))

    image_resized.save(f"app/static/images/resized_{image_path.name}")
    image_preview.save(f"app/static/images/preview_{image_path.name}")


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
) -> None:
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
