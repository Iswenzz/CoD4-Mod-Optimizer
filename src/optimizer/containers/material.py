import os
import re
import shutil

from typing import List
from pathlib import Path

from .container import Container
from ..mod import Raw


class MaterialContainer(Container):
    """
    Material container.
    """

    materials: List[str] = []
    images: List[str] = []

    def add(self, items: List[str]):
        """
        Add materials.
        """
        self.materials.extend(items)

    def process(self):
        """
        Process materials.
        """
        for material in self.materials:
            self.find_images(material)

    def find_images(self, material: str):
        """
        Find all images used by the material.
        """
        chars = r"A-Za-z0-9\-.,~_&$% "
        shortest_run = 1
        regexp = "[%s]{%d,}" % (chars, shortest_run)
        pattern = re.compile(regexp)

        path = Raw.file("materials", material)
        if not os.path.exists(path):
            return

        with open(path, "rb") as binary_file:
            data = binary_file.read().decode("ansi")
            for image in pattern.findall(data):
                if image not in self.images and image + ".iwi" in Raw.images:
                    self.images.append(image)

    def copy(self, to_path: str):
        """
        Copy materials.
        """
        print()
        print("#####################################")
        print("              Materials              ")
        print("#####################################")
        print()

        for material in self.materials:
            path = Raw.file("materials", material)
            path_properties = Raw.file("material_properties", material)
            if os.path.exists(path):
                print(material)
                shutil.copy(path, Path(to_path) / "materials" / material)
            if os.path.exists(path_properties):
                shutil.copy(
                    path_properties, Path(to_path) / "material_properties" / material
                )
