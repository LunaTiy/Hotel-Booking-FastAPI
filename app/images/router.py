import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile) -> None:
    im_path = f"app/static/images/{name}.webp"
    path = Path(im_path)

    with path.open("wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    process_picture.delay(im_path)
