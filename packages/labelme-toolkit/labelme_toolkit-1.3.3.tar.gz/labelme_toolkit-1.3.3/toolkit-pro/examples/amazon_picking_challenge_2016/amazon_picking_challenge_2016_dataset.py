import glob
import os

import imgviz
import numpy as np
from torch.utils import data

ROOT_DIR = "./amazon-picking-challenge-2016.export"


class AmazonPickingChallenge2016Dataset(data.Dataset):
    def __init__(self):
        # Find item ids in the dataset (e.g., 1466803322395175933)
        item_ids = []
        for filename in os.listdir(ROOT_DIR):
            filepath = os.path.join(ROOT_DIR, filename)
            if not os.path.isdir(filepath):
                continue
            item_id = filename
            item_ids.append(item_id)
        self.item_ids = sorted(item_ids)

        # Find label names in the dataset
        label_names = set()
        for item_id in item_ids:
            mask_paths = glob.glob(os.path.join(ROOT_DIR, item_id, "mask_*.jpg"))
            for mask_path in mask_paths:
                stem = os.path.splitext(os.path.basename(mask_path))[0]
                label_name = "_".join(stem.split("_")[2:])
                if label_name == "_container_":
                    continue
                label_names.add(label_name)
        self.label_names = sorted(label_names)

    def __len__(self):
        # Return the size of the dataset
        return len(self.item_ids)

    def __getitem__(self, index):
        item_id = self.item_ids[index]

        # Read image, bounding boxes, labels, and masks from item_id
        image_path = os.path.join(ROOT_DIR, f"{item_id}.jpg")
        mask_paths = glob.glob(os.path.join(ROOT_DIR, item_id, "mask_*.jpg"))
        #
        image = imgviz.io.imread(image_path)
        #
        labels = []  # (N,), int32
        masks = []  # (N, H, W), bool
        for mask_path in mask_paths:
            mask = imgviz.io.imread(mask_path)
            mask = (mask > 127).astype(bool)

            stem = os.path.splitext(os.path.basename(mask_path))[0]
            label_name = "_".join(stem.split("_")[2:])
            if label_name == "_container_":
                image[~mask] = 0
            else:
                masks.append(mask)
                labels.append(self.label_names.index(label_name))
        labels = np.array(labels, dtype=np.int32)
        masks = np.array(masks, dtype=bool)
        #
        bboxes = imgviz.instances.masks_to_bboxes(masks=masks).astype(
            np.float32
        )  # (N, 4), float32

        return image, bboxes, labels, masks


if __name__ == "__main__":
    data = AmazonPickingChallenge2016Dataset()
    image, bboxes, labels, masks = data[0]
    captions = [data.label_names[label] for label in labels]
    visualization = imgviz.instances2rgb(
        image,
        bboxes=bboxes,
        labels=labels,
        masks=masks,
        captions=captions,
        font_size=15,
    )
    imgviz.io.pil_imshow(visualization)
