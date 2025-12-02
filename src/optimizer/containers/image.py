import os
import shutil

from typing import List
from pathlib import Path

from .container import Container
from ..mod import Raw


class ImageContainer(Container):

    images: List[str] = []

    def add(self, items: List[str]):
        self.images.extend(items)

    def process(self):
        pass

    def copy(self, to_path: str):
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
