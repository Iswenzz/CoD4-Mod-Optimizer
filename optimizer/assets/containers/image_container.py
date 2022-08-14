from optimizer.assets.containers.i_optimizable_container import IOptimizableContainer
from optimizer.assets.raw import Raw

from typing import List
from pathlib import Path
import re, os, shutil


class ImageContainer(IOptimizableContainer):
    """
    Represent an asset container of CoD4 image IWI files.
    """

    images: List[str] = []

    def __init__(self, raw: Raw):
        """
        Initialize the ImageContainer.
        """
        self.raw = raw

    def add_items(self, items: List[str]):
        """
        Add images to the container to optimize.
        """
        self.images.extend(items)

    def optimize(self):
        """
        Optimize all images.
        """
        pass

    def copy(self, to_path: str):
        print()
        print("#####################################")
        print("               Images                ")
        print("#####################################\n")

        for image in self.images:
            from_path = self.raw.get_file("images", image + ".iwi")
            if os.path.exists(from_path):
                print(image)
                shutil.copy(from_path, Path(to_path) / "images" / (image + ".iwi"))
