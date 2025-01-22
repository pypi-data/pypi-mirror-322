import json
import os
import os.path as osp

import click
import imgviz
import numpy as np
from labelme_toolkit import _json
from labelme_toolkit import _labelme
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger

from .._labelme import group_shapes


def _export_json_file_to_yolo(
    json_file: str,
    output_dir: str,
    class_names: list[str],
):
    with open(json_file) as f:
        json_data: dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    stem = osp.splitext(osp.basename(json_file))[0]
    image_file = osp.join(output_dir, "images", f"{stem}.jpg")
    label_file = osp.join(output_dir, "labels", f"{stem}.txt")

    image: np.ndarray
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = imgviz.io.imread(image_path)
    else:
        image = _json.image_b64data_to_ndarray(json_data["imageData"])
    imgviz.io.imsave(image_file, image)
    logger.debug("[{}] Exported to {!r}", json_file, image_file)

    image_height, image_width = image.shape[:2]

    shapes: list[_labelme.Shape] = [
        _labelme.Shape(
            type=shape["shape_type"],
            points=shape["points"],
            label=shape["label"],
            group_id=shape["group_id"],
        )
        for shape in json_data["shapes"]
    ]
    grouped_shapes: list[list[_labelme.Shape]] = group_shapes(shapes=shapes)

    yolo_bboxes: list[tuple[int, float, float, float, float]] = []
    for shapes in grouped_shapes:
        if not all(shape.label == shapes[0].label for shape in shapes):
            logger.warning(
                "[{}] same group_id shapes={!r} have different labels. skipping",
                json_file,
                [shape.label for shape in shapes],
            )
            continue
        if shapes[0].label not in class_names:
            logger.warning(
                "[{}] shapes[0].label={!r} is not in class_names. skipping",
                json_file,
                shapes[0].label,
            )
            continue

        points = np.array([point for shape in shapes for point in shape.points])
        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)
        bbox_height = ymax - ymin
        bbox_width = xmax - xmin

        class_id = class_names.index(shapes[0].label)
        x_center = (xmin + xmax) / 2 / image_width
        y_center = (ymin + ymax) / 2 / image_height
        width = bbox_width / image_width
        height = bbox_height / image_height

        yolo_bboxes.append((class_id, x_center, y_center, width, height))

    with open(label_file, "w") as f:
        for class_id, x_center, y_center, width, height in yolo_bboxes:
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
    logger.debug("[{}] Exported to {!r}", json_file, label_file)


def _export_json_files_to_yolo(
    json_files: list[str],
    output_dir: str,
    class_names: list[str],
):
    if osp.exists(output_dir):
        raise FileExistsError(f"Output directory already exists: {output_dir!r}")

    os.makedirs(output_dir)

    classes_file: str = osp.join(output_dir, "classes.txt")
    with open(classes_file, "w") as f:
        f.writelines("\n".join(class_names))

    os.makedirs(osp.join(output_dir, "images"), exist_ok=True)
    os.makedirs(osp.join(output_dir, "labels"), exist_ok=True)

    for json_file in json_files:
        _export_json_file_to_yolo(
            json_file=json_file,
            output_dir=output_dir,
            class_names=class_names,
        )


def _type_class_names(value: str) -> list[str]:
    return value.split(",")


@click.command()
@click.argument("dataset_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--class-names",
    type=_type_class_names,
    required=True,
    help="class names (comma separated)",
)
def export_to_yolo(dataset_dir: str, class_names: list[str]) -> None:
    """(PRO) Export JSON files to YOLO format.

    Pass a directory that contains JSON files to convert.

    Examples:

     \b
     $ labelmetk export-to-yolo examples/small_dataset/ \
        --class-names __ignore__,bottle,bus,car,chair,person,sofa

    """
    json_files: list[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=dataset_dir
    )

    _export_json_files_to_yolo(
        json_files=json_files,
        output_dir=output_dir,
        class_names=class_names,
    )
    logger.info("[{}] Exported to {}", dataset_dir, output_dir)
