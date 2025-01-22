import glob
import json
import os.path as osp
import subprocess

from labelme_toolkit._testing import small_dataset  # noqa


def test(small_dataset):  # noqa
    subprocess.check_call(
        [
            "labelmetk",
            "rename-labels",
            small_dataset,
            "--from-to",
            "car",
            "vehicle",
            "--from-to",
            "bus",
            "vehicle",
        ]
    )

    assert osp.isdir(osp.join(small_dataset + ".export"))
    json_files = glob.glob(osp.join(small_dataset + ".export", "*.json"))
    assert len(json_files) == 3

    shapes_all = []
    for json_file in json_files:
        with open(json_file) as f:
            json_data = json.load(f)
        shapes_all.extend(json_data["shapes"])

    labels = {shape["label"] for shape in shapes_all}
    assert "vehicle" in labels
    assert "car" not in labels
    assert "bus" not in labels
