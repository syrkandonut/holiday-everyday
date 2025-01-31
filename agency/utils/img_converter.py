import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image as PILImage

from config.settings import IMG_BIG_SIZE, IMG_SMALL_SIZE, STORAGE_IMAGE_THUMB_SUB_PATH


def to_webp_and_save_thumbnail(image_field):
    image_pil = PILImage.open(image_field)

    image_io = BytesIO()

    image_pil.thumbnail(IMG_BIG_SIZE)
    image_pil.save(image_io, format="WEBP")
    image_io.seek(0)

    image_name = f"{os.path.splitext(image_field.name)[0]}.webp"
    if not os.path.exists(image_name):
        image_content_file = ContentFile(image_io.read())
        image_field.save(image_name, image_content_file, save=False)

    image_io_thumb = BytesIO()
    image_pil.thumbnail(IMG_SMALL_SIZE)
    image_pil.save(image_io_thumb, format="WEBP")
    image_io_thumb.seek(0)

    image_name_thumb = os.path.join(
        os.path.dirname(image_field.name),
        STORAGE_IMAGE_THUMB_SUB_PATH,
        os.path.splitext(os.path.basename(image_field.name))[0] + ".webp",
    )

    if not os.path.exists(image_name_thumb):
        with open(image_name_thumb, "wb") as f:
            f.write(image_io_thumb.read())
