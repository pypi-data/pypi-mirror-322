import json
import os
import os.path as osp
from typing import List

import click
import imgviz
import numpy as np
from labelme_toolkit import _json
from labelme_toolkit import _labelme
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger

from .._labelme import shapes_to_label


def _export_json_file_to_voc(
    json_file: str,
    output_dir: str,
    class_names: list[str],
    class_name_to_id: dict[str, int],
):
    with open(json_file) as f:
        json_data: dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    stem = osp.splitext(osp.basename(json_file))[0]
    image_file = osp.join(output_dir, "JPEGImages", f"{stem}.jpg")
    class_png_file = osp.join(output_dir, "SegmentationClass", f"{stem}.png")
    class_viz_file = osp.join(
        output_dir,
        "SegmentationClassVisualization",
        stem + ".jpg",
    )
    object_png_file = osp.join(output_dir, "SegmentationObject", f"{stem}.png")
    object_viz_file = osp.join(
        output_dir, "SegmentationObjectVisualization", f"{stem}.jpg"
    )

    image: np.ndarray
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = imgviz.io.imread(image_path)
    else:
        image = _json.image_b64data_to_ndarray(json_data["imageData"])
    imgviz.io.imsave(image_file, image)

    label_cls, label_obj = shapes_to_label(
        shapes=[
            _labelme.Shape(
                type=shape["shape_type"],
                points=shape["points"],
                label=shape["label"],
                group_id=shape["group_id"],
            )
            for shape in json_data["shapes"]
        ],
        image_height=json_data["imageHeight"],
        image_width=json_data["imageWidth"],
        shape_label_to_id=class_name_to_id,
    )

    # class label
    assert label_cls.min() >= -1
    assert label_cls.max() <= 255
    imgviz.io.lblsave(class_png_file, label_cls.astype(np.uint8))
    label_cls_viz = imgviz.label2rgb(
        label_cls,
        imgviz.rgb2gray(image),
        label_names=class_names,
        font_size=15,
        loc="rb",
    )
    imgviz.io.imsave(class_viz_file, label_cls_viz)

    # instance label
    assert label_obj.min() >= 0
    assert label_obj.max() <= 255
    imgviz.io.lblsave(object_png_file, label_obj.astype(np.uint8))
    instance_ids = np.unique(label_obj)
    instance_names = [str(i) for i in range(max(instance_ids) + 1)]
    insv = imgviz.label2rgb(
        label_obj,
        imgviz.rgb2gray(image),
        label_names=instance_names,
        font_size=15,
        loc="rb",
    )
    imgviz.io.imsave(object_viz_file, insv)


def _export_json_files_to_voc(
    json_files: list[str],
    output_dir: str,
    fg_class_names: list[str],
    bg_class_name: str,
    ignore_class_name: str,
):
    if os.path.exists(output_dir):
        raise ValueError(f"Output directory already exists: {output_dir}")

    os.makedirs(output_dir)
    os.makedirs(osp.join(output_dir, "JPEGImages"))
    os.makedirs(osp.join(output_dir, "SegmentationClass"))
    os.makedirs(osp.join(output_dir, "SegmentationClassVisualization"))
    os.makedirs(osp.join(output_dir, "SegmentationObject"))
    os.makedirs(osp.join(output_dir, "SegmentationObjectVisualization"))
    logger.info("Exporting to VOC format at {}", output_dir)

    class_names: list[str] = [ignore_class_name, bg_class_name]
    class_name_to_id: dict[str, int] = {ignore_class_name: -1, bg_class_name: 0}
    for class_id, class_name in enumerate(fg_class_names, start=1):
        class_names.append(class_name)
        class_name_to_id[class_name] = class_id
    logger.info("Class_names: {}", class_names)

    class_names_file = osp.join(output_dir, "class_names.txt")
    with open(class_names_file, "w") as f:
        f.writelines("\n".join(class_names))
    logger.info("Saved class_names to {!r}", class_names_file)

    for json_file in json_files:
        _export_json_file_to_voc(
            json_file=json_file,
            output_dir=output_dir,
            class_names=class_names,
            class_name_to_id=class_name_to_id,
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
@click.option(
    "--bg-class-name",
    type=str,
    default="_background_",
    help="background class name",
)
def export_to_voc(dataset_dir: str, class_names: list[str], bg_class_name: str):
    """(PRO) Export JSON files to VOC format.

    Pass a directory that contains JSON files to convert.

    Examples:

     \b
     $ labelmetk export-to-voc examples/small_dataset/ \
        --class-names __ignore__,_background_,bottle,bus,car,chair,person,sofa

    """
    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=dataset_dir
    )

    if len(class_names) > 256:
        raise ValueError(
            "maximum number of classes for VOC format is 256, use other format"
        )

    fg_class_names: list[str] = class_names[:]
    fg_class_names.remove(bg_class_name)
    fg_class_names.remove("__ignore__")

    _export_json_files_to_voc(
        json_files=json_files,
        output_dir=output_dir,
        fg_class_names=fg_class_names,
        bg_class_name=bg_class_name,
        ignore_class_name="__ignore__",
    )
