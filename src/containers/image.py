import os
import shutil

from typing import List
from pathlib import Path

from src.mod import Raw
from .container import Container


class ImageContainer(Container):
    """
    Image container.
    """

    images: List[str] = []

    def add(self, items: List[str]):
        """
        Add images.
        """
        self.images.extend(items)

    def process(self):
        """
        Process images.
        """

    def copy(self, to_path: str):
        """
        Copy images.
        """
        print()
        print("#####################################")
        print("               Images                ")
        print("#####################################")
        print()

        for image in self.images:
            from_path = Raw.file("images", image + ".iwi")
            if os.path.exists(from_path):
                print(image)
                shutil.copy(from_path, Path(to_path) / "images" / (image + ".iwi"))
