import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_setup import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_picture(
        path: str,
) -> None:
    image_path = Path(path)
    image = Image.open(image_path)

    image_resized = image.resize((1000, 500))
    image_preview = image.resize((200, 100))

    image_resized.save(f"app/static/images/resized_{image_path.name}")
    image_preview.save(f"app/static/images/preview_{image_path.name}")


@celery_app.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
) -> None:
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(msg_content)
