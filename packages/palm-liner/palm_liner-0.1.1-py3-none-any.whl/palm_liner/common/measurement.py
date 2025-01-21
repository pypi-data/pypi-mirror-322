from typing import Any, List

from PIL import Image, ImageDraw
from PIL.ImageFile import ImageFile


def get_lines_wraped(
    image_warped_clean_mini: ImageFile,
    palm_lines: List[Any],
    line_width: int,
) -> ImageFile:
    image = Image.new(mode="RGB", size=image_warped_clean_mini.size, color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    heart_line = palm_lines[0]
    head_line = palm_lines[1]
    life_line = palm_lines[2]

    heart_line_points = [tuple(reversed(l[:2])) for l in heart_line]
    draw.line(heart_line_points, fill="white", width=line_width)

    head_line_points = [tuple(reversed(l[:2])) for l in head_line]
    draw.line(head_line_points, fill="white", width=line_width)

    life_line_points = [tuple(reversed(l[:2])) for l in life_line]
    draw.line(life_line_points, fill="white", width=line_width)

    return image
