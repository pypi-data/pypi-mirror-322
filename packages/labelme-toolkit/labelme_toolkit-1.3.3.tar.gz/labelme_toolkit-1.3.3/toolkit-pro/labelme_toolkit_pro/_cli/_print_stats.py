import json
import uuid
from typing import Dict
from typing import List

import click
import numpy as np
import pandas
import tabulate
from labelme_toolkit import _migrations
from labelme_toolkit import _paths


def _print_stats(json_files: List[str]):
    data = []
    for json_file in json_files:
        with open(json_file, "r") as f:
            json_data = json.load(f)
        _migrations.migrate_json_data(json_data=json_data)

        group_id_num_to_uuid: Dict[int, str] = {}
        for shape in json_data["shapes"]:
            if shape["group_id"] is None:
                group_id = str(uuid.uuid1())
            else:
                group_id = group_id_num_to_uuid.get(
                    shape["group_id"], str(uuid.uuid1())
                )
                group_id_num_to_uuid[shape["group_id"]] = group_id

            data.append(
                {
                    "file": json_file,
                    "imageWidth": json_data["imageWidth"],
                    "imageHeight": json_data["imageHeight"],
                    "label": shape["label"],
                    "group_id": group_id,
                }
            )
    df = pandas.DataFrame(data)

    df_files = df.groupby("file")[["imageWidth", "imageHeight"]].first()
    df_shapes = df.drop(columns=["imageWidth", "imageHeight"])

    print()
    print("# overall")
    #
    # overall (files)
    rows = []
    for key, value in [
        ("imageWidth", df_files["imageWidth"]),
        ("imageHeight", df_files["imageHeight"]),
        (
            "min(imageWidth, imageHeight)",
            np.minimum(df_files["imageWidth"], df_files["imageHeight"]),
        ),
        (
            "max(imageWidth, imageHeight)",
            np.maximum(df_files["imageWidth"], df_files["imageHeight"]),
        ),
        (
            "sqrt(imageWidth * imageHeight)",
            np.sqrt(df_files["imageWidth"] * df_files["imageHeight"]),
        ),
    ]:
        rows.append((key, value.mean(), value.min(), value.max()))
    print(
        tabulate.tabulate(
            rows, headers=["average", "min", "max"], tablefmt="fancy_outline"
        )
    )
    #
    # overall (shapes)
    num_shapes = df_shapes.shape[0]
    num_groups = df_shapes.groupby(["file", "group_id"]).count().shape[0]
    num_shapes_per_file = num_shapes / df_shapes["file"].unique().shape[0]
    num_groups_per_file = (
        df_shapes.groupby(["file", "group_id"])
        .count()
        .groupby("file")
        .count()
        .mean()
        .item()
    )
    num_shapes_per_label = df_shapes.groupby("label").count()["file"].mean()
    num_groups_per_label = (
        df_shapes.groupby(["label", "group_id"])
        .count()
        .groupby("label")
        .count()
        .mean()
        .item()
    )
    rows = [
        ("# of shapes", num_shapes, num_shapes_per_file, num_shapes_per_label),
        ("# of groups", num_groups, num_groups_per_file, num_groups_per_label),
    ]
    print()
    print(
        tabulate.tabulate(
            rows,
            headers=["", "total", "per file", "per label"],
            tablefmt="fancy_outline",
        )
    )

    # per label
    num_shapes_per_label = (
        df_shapes.groupby("label").count().drop(columns="group_id")["file"]
    )
    num_groups_per_label = (
        df_shapes.groupby(["label", "group_id"])
        .count()
        .groupby("label")
        .count()["file"]
    )
    df_per_label = pandas.concat([num_shapes_per_label, num_groups_per_label], axis=1)
    del num_shapes_per_label, num_groups_per_file
    df_per_label.columns = ["# of shapes", "# of groups"]
    print()
    print("# per label")
    print(tabulate.tabulate(df_per_label, headers="keys", tablefmt="fancy_outline"))
    del df_per_label

    # per file
    num_shapes_per_label = df_shapes.groupby("file").count().drop(columns="group_id")
    df_num_groups = (
        df_shapes.groupby(["file", "group_id"]).count().groupby("file").count()
    )
    df_per_file = pandas.concat([df_files, num_shapes_per_label, df_num_groups], axis=1)
    del num_shapes_per_label, df_num_groups
    df_per_file.columns = ["imageWidth", "imageHeight", "# of shapes", "# of groups"]
    print()
    print("# per file")
    print(tabulate.tabulate(df_per_file, headers="keys", tablefmt="fancy_outline"))
    del df_per_file

    # per file, per label
    df_num_shapes_per_file_and_label = df_shapes.groupby(["file", "label"]).count()
    df_num_groups_per_file_and_label = df_shapes.groupby(["file", "label"]).nunique()
    df_per_file_and_label = pandas.concat(
        [df_num_shapes_per_file_and_label, df_num_groups_per_file_and_label],
        axis=1,
    )
    df_per_file_and_label.columns = ["# of shapes", "# of groups"]
    print()
    print("# per file & label")
    print(
        tabulate.tabulate(
            df_per_file_and_label, headers="keys", tablefmt="fancy_outline"
        )
    )


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
def print_stats(file_or_dir) -> None:
    """(PRO) Print statistics about JSON files.

    Pass a JSON file or directory to print statistics.

    Examples:

     \b
     $ labelmetk print-stats examples/small_dataset/2011_000003.json
     $ labelmetk print-stats examples/small_dataset/

    """
    json_files: List[str]
    json_files, _ = _paths.get_json_files_and_output_dir(file_or_dir=file_or_dir)
    _print_stats(json_files=json_files)
