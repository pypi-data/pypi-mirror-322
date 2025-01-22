import functools
import json
import os
from typing import Dict
from typing import List
from typing import Optional

import click
import numpy as np
import PIL.Image
from labelme_toolkit import _browsers
from labelme_toolkit import _labelme
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger

from .._labelme import group_shapes


def _json_to_masks(
    json_file: str,
    output_dir: str,
    exclude_labels: Optional[List[str]] = None,
) -> List[str]:
    if exclude_labels is None:
        exclude_labels = []

    with open(json_file) as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    shapes: list[_labelme.Shape] = [
        _labelme.Shape(
            type=shape_json["shape_type"],
            points=shape_json["points"],
            label=shape_json["label"],
            group_id=shape_json["group_id"],
        )
        for shape_json in json_data["shapes"]
        if shape_json["label"] not in exclude_labels
    ]

    grouped_shapes: list[list[_labelme.Shape]] = group_shapes(shapes=shapes)

    output_dir = os.path.join(
        output_dir, os.path.splitext(os.path.basename(json_file))[0]
    )
    os.makedirs(output_dir, exist_ok=True)

    output_files = []
    for i, shapes in enumerate(grouped_shapes):
        mask: np.ndarray = functools.reduce(
            np.logical_or,
            (
                _labelme.shape_to_mask(
                    shape=shape,
                    image_height=json_data["imageHeight"],
                    image_width=json_data["imageWidth"],
                )
                for shape in shapes
            ),
        )

        output_file = os.path.join(output_dir, f"mask_{i}_{shapes[0].label}.jpg")
        PIL.Image.fromarray(mask.astype(np.uint8) * 255).save(output_file)
        logger.info(f"Saved to: {output_file!r}")
        output_files.append(output_file)

    return output_files


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--exclude-labels",
    type=str,
    multiple=True,
    help="labels to exclude",
    default=None,
)
@click.option(
    "--browse",
    "-b",
    is_flag=True,
    help="browse the output files",
)
def json_to_masks(file_or_dir, exclude_labels, browse: bool):
    """(PRO) Convert JSON file to a mask per shape.

    Pass a JSON file or directory to convert.

    Examples:

     \b
     $ labelmetk json-to-masks examples/small_dataset/2011_000003.json
     $ labelmetk json-to-masks examples/small_dataset/

    """
    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )

    json_file_to_output_files: Dict[str, List[str]] = {}
    for json_file in json_files:
        json_file_to_output_files[json_file] = _json_to_masks(
            json_file=json_file,
            output_dir=output_dir,
            exclude_labels=exclude_labels,
        )

    if browse and json_file_to_output_files:
        _browsers.browse_images(
            image_paths_per_group=json_file_to_output_files, prefix="json-to-masks-"
        )
