from pathlib import Path

from PIL import Image

from app.tasks.celery_setup import celery


@celery.task
def process_picture(
        path: str,
):
    image_path = Path(path)
    image = Image.open(image_path)

    image_resized = image.resize((1000, 500))
    image_preview = image.resize((200, 100))

    image_resized.save(f"app/static/images/resized_{image_path.name}")
    image_preview.save(f"app/static/images/preview_{image_path.name}")
