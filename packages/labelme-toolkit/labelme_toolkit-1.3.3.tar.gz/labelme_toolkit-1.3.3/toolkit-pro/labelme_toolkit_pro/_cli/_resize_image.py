import json
import os
from typing import Dict
from typing import List
from typing import Tuple

import click
import numpy as np
import PIL.Image
from labelme_toolkit import _json
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger

from labelme_toolkit_pro import _labelme


def _resize_image(json_file: str, output_dir: str, scale: float) -> None:
    with open(json_file) as f:
        json_data = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    image: PIL.Image.Image
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = PIL.Image.open(image_path)
    else:
        image = PIL.Image.fromarray(
            _json.image_b64data_to_ndarray(json_data["imageData"])
        )

    dst_size: Tuple[int, int] = tuple(
        (np.array(image.size) * scale).round().astype(int)
    )
    #
    image = image.resize(size=dst_size, resample=PIL.Image.BILINEAR)
    json_data["imageHeight"] = image.height
    json_data["imageWidth"] = image.width
    if json_data["imageData"] is not None:
        json_data["imageData"] = _json.image_ndarray_to_b64data(np.asarray(image))
    #
    json_shape: Dict
    for json_shape in json_data["shapes"]:
        shape: _labelme.Shape = _labelme.Shape(
            type=json_shape["shape_type"],
            label=json_shape["label"],
            points=json_shape["points"],
        )
        shape = _labelme.resize_shape(shape=shape, scale=scale)
        json_shape["points"] = shape.points.tolist()

    os.makedirs(output_dir, exist_ok=True)
    #
    image_file = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
    if os.path.exists(image_file):
        output_image_file = os.path.join(
            output_dir, os.path.splitext(os.path.basename(json_file))[0] + ".jpg"
        )
        image.save(output_image_file)
        logger.info(f"{json_file} - Saved to {output_image_file!r}")
        json_data["imagePath"] = os.path.basename(output_image_file)
    #
    output_json_file = os.path.join(output_dir, os.path.basename(json_file))
    with open(output_json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"{json_file} - Saved to {output_json_file!r}")


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--scale",
    type=float,
    help="Scale factor for resizing image",
    required=True,
)
def resize_image(file_or_dir, scale) -> None:
    """(PRO) Resize image and shapes in JSON files.

    Pass a JSON file or directory to resize.

    Examples:

     \b
     $ labelmetk resize-image examples/small_dataset/2011_000003.json
     $ labelmetk resize-image examples/small_dataset/

    """
    logger.info(f"Resizing image and shapes with scale: {scale}")

    json_files: List[str]
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )

    json_file: str
    for json_file in json_files:
        _resize_image(json_file=json_file, output_dir=output_dir, scale=scale)
