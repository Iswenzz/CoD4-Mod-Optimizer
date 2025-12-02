import os
import shutil
import sys

from pathlib import Path

from .mod import Raw, CSV
from .containers import ImageContainer, MaterialContainer, XModelContainer

HELP_MESSAGE = """
CoD4 Mod Optimizer (c) Iswenzz 2018-2024
Usage: ptimizer.exe <input path> <output path>
"""


def process(in_path: str, out_path: str):
    folders = ["materials", "material_properties", "xmodel", "images"]

    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    os.mkdir(out_path)

    if not os.path.exists(in_path):
        os.mkdir(in_path)

    for folder in folders:
        os.mkdir(Path(out_path) / folder)
        if not os.path.exists(Path(in_path) / folder):
            os.mkdir(Path(in_path) / folder)

    if not os.path.exists(Path(in_path) / "mod.csv"):
        print("ERROR: Mod CSV not found.")
        sys.exit()

    Raw.initialize(in_path)
    csv = CSV(Path(in_path) / "mod.csv")

    image = ImageContainer()
    material = MaterialContainer()
    xmodel = XModelContainer()

    xmodel.add(csv["xmodel"])
    xmodel.process()
    xmodel.copy(out_path)

    material.add(csv["material"])
    material.add(xmodel.materials)
    material.process()
    material.copy(out_path)

    image.add(csv["image"])
    image.add(material.images)
    image.process()
    image.copy(out_path)


def main():
    in_path = "in"
    out_path = "out"

    if len(sys.argv) == 3:
        in_path = sys.argv[1]
        out_path = sys.argv[2]
    else:
        print(HELP_MESSAGE)
        sys.exit(-1)

    process(in_path, out_path)
