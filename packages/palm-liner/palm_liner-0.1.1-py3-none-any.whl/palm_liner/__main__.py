import argparse
from pathlib import Path

from palm_liner import PalmLiner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="the path to the input image")
    parser.add_argument("--output", required=True, help="the path to the output image")

    args = parser.parse_args()

    input_image = Path(args.input).resolve()
    output_image = Path(args.output).resolve()

    assert input_image.exists(), f"File not found {input_image}"

    temp_dir = Path("temp").resolve()
    temp_dir.mkdir(parents=True, exist_ok=True)

    palm_liner_client = PalmLiner(
        line_color=(119, 253, 153, 255),
        line_width=3,
    )

    with open(input_image, "rb") as f:
        image_original = f.read()

    image_lines = palm_liner_client.get_palm_lines(image_original=image_original)

    with open(output_image, "wb") as f:
        f.write(image_lines)


if __name__ == "__main__":
    main()
