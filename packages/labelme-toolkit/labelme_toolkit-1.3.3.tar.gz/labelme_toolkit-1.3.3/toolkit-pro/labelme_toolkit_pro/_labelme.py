import collections
import functools

import numpy as np
from labelme_toolkit._labelme import Shape
from labelme_toolkit._labelme import shape_to_mask


def resize_shape(shape: Shape, scale: float) -> Shape:
    if shape.type in ["circle", "rectangle", "polygon"]:
        points = shape.points * scale
        return Shape(type=shape.type, points=points, label=shape.label)
    else:
        raise ValueError(f"Unsupported shape type={shape.type!r}")


def group_shapes(shapes: list[Shape]) -> list[list[Shape]]:
    unique_group_ids = set(
        shape.group_id for shape in shapes if shape.group_id is not None
    )

    grouped_shapes = collections.defaultdict(list)
    for shape in shapes:
        if shape.group_id is None:
            shape.group_id = max(unique_group_ids, default=0) + 1
            unique_group_ids.add(shape.group_id)
        grouped_shapes[shape.group_id].append(shape)

    return list(grouped_shapes.values())


def shapes_to_label(
    shapes: list[Shape],
    image_height: int,
    image_width: int,
    shape_label_to_id: dict[str, int],
) -> tuple[np.ndarray, np.ndarray]:
    IGNORE_CLASS_ID: int = -1
    BG_CLASS_ID: int = 0
    if any(shape_label_to_id[shape.label] == BG_CLASS_ID for shape in shapes):
        unannotated_area_class_id = IGNORE_CLASS_ID
    else:
        unannotated_area_class_id = BG_CLASS_ID

    label_cls: np.ndarray = np.full(
        (image_height, image_width), unannotated_area_class_id, dtype=np.int32
    )
    for shape in shapes:
        mask = shape_to_mask(
            shape=shape, image_height=image_height, image_width=image_width
        )
        label_cls[mask] = shape_label_to_id[shape.label]

    label_obj: np.ndarray = np.zeros((image_height, image_width), dtype=np.int32)
    grouped_shapes: list[list[Shape]] = group_shapes(shapes=shapes)
    for object_id, shapes in enumerate(grouped_shapes, start=1):
        mask: np.ndarray = functools.reduce(
            np.logical_or,
            (
                shape_to_mask(
                    shape=shape, image_height=image_height, image_width=image_width
                )
                for shape in shapes
            ),
        )
        label_obj[mask] = object_id

    return label_cls, label_obj
