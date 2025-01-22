import json
import os
from typing import Dict
from typing import List
from typing import Optional

import click
import imgviz
import numpy as np
import osam.apis
import osam.types
import PIL.Image
from labelme_toolkit import _json
from labelme_toolkit import _labelme
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger


def _shape_rectangle_to_mask(
    shape: _labelme.Shape,
    image: np.ndarray,
    image_embedding: Optional[Dict] = None,
    keep_original_bounding_box: bool = False,
):
    if shape.type != "rectangle":
        raise ValueError(f"shape.type={shape.type!r} is not 'rectangle'")

    (x1, y1), (x2, y2) = shape.points
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)

    request = osam.types.GenerateRequest(
        model="efficientsam",
        image_embedding=image_embedding,
        image=image,
        prompt=osam.types.Prompt(
            points=[[xmin, ymin], [xmax, ymax]], point_labels=[2, 3]
        ),
    )
    response = osam.apis.generate(request=request)

    mask = response.annotations[0].mask

    if keep_original_bounding_box:
        height, width = image.shape[:2]
        xmin = np.clip(int(xmin), 0, width - 1)
        xmax = np.clip(int(np.ceil(xmax)), 0, width - 1)
        ymin = np.clip(int(ymin), 0, height - 1)
        ymax = np.clip(int(np.ceil(ymax)), 0, height - 1)
    else:
        ymin, xmin, ymax, xmax = imgviz.instances.masks_to_bboxes([mask])[0].astype(int)

    shape_mask = _labelme.Shape(
        type="mask",
        points=[[xmin, ymin], [xmax, ymax]],
        label=shape.label,
        mask=mask[ymin : ymax + 1, xmin : xmax + 1],
    )

    return shape_mask, response.image_embedding


def _ai_rectangle_to_mask(
    json_file: str,
    output_dir: str,
    keep_original_bounding_box: bool,
):
    with open(json_file) as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    image: np.ndarray
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = np.asarray(PIL.Image.open(image_path))
    else:
        image = _json.image_b64data_to_ndarray(json_data["imageData"])

    image_embedding = None

    for i, json_shape in enumerate(json_data["shapes"]):
        if json_shape["shape_type"] != "rectangle":
            continue

        shape_rectangle = _labelme.Shape(
            type=json_shape["shape_type"],
            points=json_shape["points"],
            label=json_shape["label"],
        )
        shape_mask, image_embedding = _shape_rectangle_to_mask(
            shape=shape_rectangle,
            image=image,
            image_embedding=image_embedding,
            keep_original_bounding_box=keep_original_bounding_box,
        )

        json_data["shapes"][i] = shape_mask.to_json()

    os.makedirs(output_dir, exist_ok=True)
    #
    output_json_file = os.path.join(output_dir, os.path.basename(json_file))
    with open(output_json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"{json_file} - Saved to {output_json_file!r}")

    if json_data["imageData"] is None:
        output_image_file = os.path.join(output_dir, json_data["imagePath"])
        PIL.Image.fromarray(image).save(output_image_file)
        logger.info(f"{json_file} - Saved to {output_image_file!r}")


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--keep-original-bounding-box",
    is_flag=True,
    help="keep the original bounding box",
)
def ai_rectangle_to_mask(file_or_dir: str, keep_original_bounding_box: bool):
    """(PRO) Convert rectangle shape to masks by AI.

    Pass a JOSN file or a directory to convert.

    Examples:

     \b
     $ labelme-toolkit-pro ai-rectangle-to-mask dogs_rectangles.json

    """
    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )

    for json_file in json_files:
        _ai_rectangle_to_mask(
            json_file=json_file,
            output_dir=output_dir,
            keep_original_bounding_box=keep_original_bounding_box,
        )
