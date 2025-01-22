import re
import subprocess

from labelme_toolkit._testing import small_dataset  # noqa


def test(small_dataset):  # noqa
    output = subprocess.check_output(
        ["labelmetk", "print-stats", small_dataset]
    ).decode()

    assert re.search(r"# of shapes.*18", output)
    assert re.search(r"# of groups.*14", output)
