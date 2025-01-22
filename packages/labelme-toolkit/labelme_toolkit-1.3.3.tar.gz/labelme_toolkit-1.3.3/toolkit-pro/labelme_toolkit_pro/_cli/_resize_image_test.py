import glob
import json
import os.path as osp
import subprocess

import numpy as np
import PIL.Image
from labelme_toolkit._testing import small_dataset  # noqa


def test(small_dataset):  # noqa
    scale = 0.5

    subprocess.check_call(
        [
            "labelmetk",
            "resize-image",
            small_dataset,
            f"--scale={scale}",
        ]
    )

    assert osp.isdir(osp.join(small_dataset + ".export"))
    json_files = glob.glob(osp.join(small_dataset + ".export", "*.json"))
    assert len(json_files) == 3

    for json_file in json_files:
        with open(json_file) as f:
            json_data = json.load(f)

        original_json_file = osp.join(small_dataset, osp.basename(json_file))
        with open(original_json_file) as f:
            original_json_data = json.load(f)

        assert json_data["imageHeight"] == int(
            round(original_json_data["imageHeight"] * scale)
        )
        assert json_data["imageWidth"] == int(
            round(original_json_data["imageWidth"] * scale)
        )

        image_file = osp.join(osp.dirname(json_file), json_data["imagePath"])
        image = np.asarray(PIL.Image.open(image_file))
        assert image.shape[0] == json_data["imageHeight"]
        assert image.shape[1] == json_data["imageWidth"]
