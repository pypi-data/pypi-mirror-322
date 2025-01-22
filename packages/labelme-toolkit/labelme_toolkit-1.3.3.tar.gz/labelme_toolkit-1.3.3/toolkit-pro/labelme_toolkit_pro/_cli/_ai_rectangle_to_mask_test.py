import json
import pathlib
import shutil
import subprocess

import labelme_toolkit
import pytest


@pytest.fixture
def dogs_rectangle_json_file(tmp_path: pathlib.Path):
    dogs_rectangle_json_file = (
        pathlib.Path(labelme_toolkit.__file__).parent / "_data/dogs_rectangle.json"
    )
    shutil.copy(dogs_rectangle_json_file, tmp_path)
    return tmp_path / dogs_rectangle_json_file.name


def test(dogs_rectangle_json_file: pathlib.Path):
    subprocess.check_call(
        ["labelmetk", "ai-rectangle-to-mask", dogs_rectangle_json_file]
    )

    output_dir: pathlib.Path = (
        dogs_rectangle_json_file.parent / f"{dogs_rectangle_json_file.stem}.export"
    )

    output_json_file = output_dir / dogs_rectangle_json_file.name
    assert output_json_file.exists()

    with open(output_json_file) as f:
        json_data = json.load(f)

    assert len(json_data["shapes"]) == 3
    for shape in json_data["shapes"]:
        assert shape["shape_type"] == "mask"
        assert "points" in shape
        assert "label" in shape
        assert "mask" in shape
