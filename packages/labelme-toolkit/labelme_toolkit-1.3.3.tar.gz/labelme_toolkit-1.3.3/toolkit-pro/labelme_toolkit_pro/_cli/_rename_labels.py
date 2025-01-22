import json
import os
import shutil
from typing import Dict
from typing import List
from typing import Tuple

import click
from labelme_toolkit import _migrations
from labelme_toolkit import _paths
from loguru import logger


def _rename_labels(
    json_file: str, output_dir: str, from_to: List[Tuple[str, str]]
) -> None:
    with open(json_file) as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    for shape in json_data["shapes"]:
        for from_label, to_label in from_to:
            if shape["label"] == from_label:
                logger.debug(f"{json_file} - Renaming {from_label!r} to {to_label!r}")
                shape["label"] = to_label
                break

    os.makedirs(output_dir, exist_ok=True)

    output_json_file = os.path.join(output_dir, os.path.basename(json_file))
    with open(output_json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"{json_file} - Saved to {output_json_file!r}")

    image_file = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
    if os.path.exists(image_file):
        shutil.copy(image_file, output_dir)
        logger.info(f"{json_file} - Copied image to {output_dir!r}")


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--from-to",
    nargs=2,
    multiple=True,
    help="pairs of from_label to_label",
    default=None,
    required=True,
)
def rename_labels(file_or_dir, from_to: List[Tuple[str, str]]) -> None:
    """(PRO) Rename labels in JSON files.

    Pass a JSON file or directory to rename labels.

    Examples:

     \b
     $ labelmetk print-stats examples/small_dataset/2011_000003.json --from-to chair sofa
     $ labelmetk print-stats examples/small_dataset/ --from-to car vehicle --from-to bus vehicle

    """  # noqa
    logger.info(f"Renaming labels: {from_to}")

    json_files: List[str]
    json_files, output_dir = _paths.get_json_files_and_output_dir(file_or_dir)

    json_file: str
    for json_file in json_files:
        _rename_labels(json_file=json_file, output_dir=output_dir, from_to=from_to)
