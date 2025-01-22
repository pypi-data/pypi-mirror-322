import glob
import os.path as osp
import re
import subprocess

import numpy as np
import PIL.Image
from labelme_toolkit._testing import small_dataset  # noqa


def test(small_dataset):  # noqa
    subprocess.check_call(["labelmetk", "json-to-masks", small_dataset])

    assert osp.isdir(osp.join(small_dataset + ".export"))
    mask_files = glob.glob(osp.join(small_dataset + ".export", "*/mask_*.jpg"))
    assert len(mask_files) == 14

    for mask_file in mask_files:
        basename = osp.basename(mask_file)
        assert re.match(r"mask_\d+_.+\.jpg", basename)

        mask = np.asarray(PIL.Image.open(mask_file))
        assert mask.dtype == np.uint8
        assert mask.ndim == 2
