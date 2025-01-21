from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from PIL.ImageFile import ImageFile
import cv2
from pillow_heif import register_heif_opener


def heic_to_jpeg(
    heic_dir: Path,
    jpeg_dir: Path,
):
    register_heif_opener()
    image = Image.open(heic_dir)
    image.save(jpeg_dir, "JPEG")


def remove_background(image_warped: cv2.typing.MatLike) -> cv2.typing.MatLike:
    hsv = cv2.cvtColor(image_warped, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 20, 80], dtype="uint8")
    upper = np.array([50, 255, 255], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image_warped, image_warped, mask=mask)
    b, g, r = cv2.split(result)
    filter = g.copy()
    ret, mask = cv2.threshold(filter, 10, 255, 1)
    image_warped[mask == 255] = 255

    return image_warped


def resize_image(
    image_warped_clean: cv2.typing.MatLike,
    resize_value: int,
) -> ImageFile:
    image_pil = Image.fromarray(cv2.cvtColor(image_warped_clean, cv2.COLOR_BGR2RGB))

    return image_pil.resize((resize_value, resize_value), resample=Image.NEAREST)


def get_palm_lines_original(
    image_warped_clean: cv2.typing.MatLike,
    image_palm_lines_wrapped: ImageFile,
    line_color: Tuple[int, int, int],
) -> ImageFile:
    image_warped_clean_pil = Image.fromarray(
        cv2.cvtColor(image_warped_clean, cv2.COLOR_BGR2RGB),
    )

    restored_img = image_palm_lines_wrapped.resize(
        image_warped_clean_pil.size, resample=Image.NEAREST
    ).convert("RGBA")

    data = restored_img.getdata()
    new_data = []

    for item in data:
        if item[:3] == (0, 0, 0):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    restored_img.putdata(new_data)

    smoothed_image = restored_img.filter(ImageFilter.MedianFilter(size=5))

    blurred_image = smoothed_image.filter(ImageFilter.GaussianBlur(radius=5))

    grayscale_image = blurred_image.convert("L")
    binary_image = grayscale_image.point(lambda p: p > 128 and 255)

    enhancer = ImageEnhance.Contrast(binary_image)
    high_contrast_image = enhancer.enhance(2)

    high_contrast_image = high_contrast_image.convert("RGBA")

    data = high_contrast_image.getdata()
    new_data = []

    for item in data:
        if item[:3] == (0, 0, 0):
            new_data.append((0, 0, 0, 0))
        elif item[:3] == (255, 255, 255):
            new_data.append(line_color)
        else:
            new_data.append(item)

    high_contrast_image.putdata(new_data)

    return high_contrast_image
