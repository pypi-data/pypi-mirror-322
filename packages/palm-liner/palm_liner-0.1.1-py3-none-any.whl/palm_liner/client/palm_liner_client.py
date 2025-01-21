import io
import logging
from pathlib import Path
from typing import Tuple

from PIL.ImageFile import ImageFile

from palm_liner.client.exceptions import GetPalmLinesError
from palm_liner.common.classification import get_lines
from palm_liner.common.detection import detect_lines
from palm_liner.common.measurement import get_lines_wraped
from palm_liner.common.model import get_u_net
from palm_liner.common.rectification import get_image_warped
from palm_liner.common.tools import (
    get_palm_lines_original,
    remove_background,
    resize_image,
)


class PalmLiner:
    def __init__(self, line_color: Tuple[int], line_width: int) -> None:
        """
        Initializator for PalmLiner.

        :param line_color: Line color in RGBA format.
        :param line_width: Line width.
        """

        self.line_color = line_color
        self.line_width = line_width

    def get_palm_lines(self, image_original: bytes) -> bytes:
        resize_value = 256
        path_to_model = (
            Path(__file__).parent.parent / "checkpoint" / "checkpoint_aug_epoch70.pth"
        )

        assert path_to_model.exists(), "File with model not found!"

        logging.info("Trying to get image with palm lines")

        try:
            image_warped = get_image_warped(image_original=image_original)

            image_warped_clean = remove_background(image_warped=image_warped)
            image_warped_clean_mini = resize_image(
                image_warped_clean=image_warped_clean,
                resize_value=resize_value,
            )

            u_net = get_u_net(
                path_to_model=path_to_model,
                n_channels=3,
                n_classes=1,
            )

            image_palm_lines = detect_lines(
                u_net=u_net,
                image_warped_clean_mini=image_warped_clean_mini,
            )

            palm_lines = get_lines(image_palm_lines=image_palm_lines)

            image_palm_lines_wrapped = get_lines_wraped(
                image_warped_clean_mini=image_warped_clean_mini,
                palm_lines=palm_lines,
                line_width=self.line_width,
            )
            
            image_palm_lines_postproducted = get_palm_lines_original(
                image_warped_clean=image_warped_clean,
                image_palm_lines_wrapped=image_palm_lines_wrapped,
                line_color=self.line_color,
            )
        except Exception as e:
            logging.error(f"Error while recieving image with palm lines: {e}")

            raise GetPalmLinesError()

        logging.info("Image with palm lines recieved successfuly")

        return self.__image_to_bytes(image_palm_lines_postproducted)

    def __image_to_bytes(self, image: ImageFile) -> bytes:
        bytes_io = io.BytesIO()

        image.save(bytes_io, "png")

        return bytes_io.getvalue()
