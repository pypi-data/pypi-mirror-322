import subprocess

from labelme_toolkit._testing import small_dataset  # noqa


def test(small_dataset):  # noqa
    subprocess.check_call(
        [
            "labelmetk",
            "export-to-voc",
            small_dataset,
            "--class-names",
            "__ignore__,_background_,bottle,bus,car,chair,person,sofa",
        ]
    )
