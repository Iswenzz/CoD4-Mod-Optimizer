import os
import re
import shutil

from typing import List
from pathlib import Path

from .container import Container
from ..mod import Raw


class XModelContainer(Container):

    xmodels: List[str] = []
    materials: List[str] = []

    def add(self, items: List[str]):
        self.xmodels.extend(items)

    def process(self):
        for xmodel in self.xmodels:
            self.find_materials(xmodel)

    def find_materials(self, xmodel: str):
        chars = r"A-Za-z0-9\-.,~_&$% "
        shortest_run = 1
        regexp = "[%s]{%d,}" % (chars, shortest_run)
        pattern = re.compile(regexp)

        path = Raw.file("xmodel", xmodel)
        if not os.path.exists(path):
            return

        with open(path, "rb") as binary_file:
            data = binary_file.read().decode("ansi")
            for material in pattern.findall(data):
                if material not in self.materials and material in Raw.materials:
                    self.materials.append(material)

    def copy(self, to_path: str):
        print()
        print("#####################################")
        print("               XModels               ")
        print("#####################################")
        print()

        for xmodel in self.xmodels:
            path = Raw.file("xmodel", xmodel)
            if os.path.exists(path):
                print(xmodel)
                shutil.copy(path, Path(to_path) / "xmodel" / xmodel)
