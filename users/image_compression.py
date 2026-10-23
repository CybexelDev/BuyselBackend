import io
import os

from PIL import Image, ImageOps, UnidentifiedImageError
from django.core.files.uploadedfile import SimpleUploadedFile


MAX_IMAGE_SIZE = 120 * 1024


def compress_image(uploaded_file):
    if not uploaded_file:
        return uploaded_file

    content_type = getattr(uploaded_file, "content_type", "") or ""

    if not content_type.startswith("image/"):
        return uploaded_file

    try:
        uploaded_file.seek(0)

        with Image.open(uploaded_file) as original:
            image = ImageOps.exif_transpose(original)
            image.load()

            if image.mode in ("RGBA", "LA") or (
                image.mode == "P" and "transparency" in image.info
            ):
                rgba = image.convert("RGBA")
                background = Image.new("RGB", rgba.size, (255, 255, 255))
                background.paste(rgba, mask=rgba.getchannel("A"))
                image = background
            else:
                image = image.convert("RGB")

            max_dimension = 2400
            quality = 85

            while True:
                current = image.copy()

                if max(current.size) > max_dimension:
                    current.thumbnail(
                        (max_dimension, max_dimension),
                        Image.Resampling.LANCZOS,
                    )

                output = io.BytesIO()
                current.save(
                    output,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                    progressive=True,
                )

                data = output.getvalue()

                if len(data) <= MAX_IMAGE_SIZE:
                    break

                if quality > 30:
                    quality = max(quality - 10, 30)
                else:
                    max_dimension = int(max_dimension * 0.75)
                    quality = 70

                if max_dimension < 100:
                    raise ValueError(
                        "Unable to compress image to 150 KB."
                    )

            filename = os.path.splitext(uploaded_file.name)[0] + ".jpg"

            return SimpleUploadedFile(
                name=filename,
                content=data,
                content_type="image/jpeg",
            )

    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError(
            f"Could not compress '{uploaded_file.name}': {exc}"
        ) from exc

    finally:
        try:
            uploaded_file.seek(0)
        except (AttributeError, OSError):
            pass
