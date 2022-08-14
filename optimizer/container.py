from optimizer import Raw, CSV, ImageContainer, MaterialContainer, XModelContainer

from pathlib import Path
import os, shutil, sys


class Container:
    """
    Represent the optimizer container with all assets.
    """

    def __init__(self, in_path: str, out_path: str):
        """
        Initialize the Optimizer instance.
        """
        self.in_path = in_path
        self.out_path = out_path

        self.raw = Raw(in_path)
        self.csv = CSV(Path(in_path) / "mod.csv")

        self.material_container = MaterialContainer(self.raw)
        self.xmodel_container = XModelContainer(self.raw)
        self.image_container = ImageContainer(self.raw)

        self.optimize()

    def initialize_folders(self):
        """
        Setup all necessary folders and check if a mod CSV exists.
        """
        folders = ["materials", "material_properties", "xmodel", "images"]

        if not os.path.exists(self.in_path):
            os.mkdir(self.in_path)
        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)

        for folder in folders:
            if not os.path.exists(Path(self.in_path) / folder):
                os.mkdir(Path(self.in_path) / folder)
            if os.path.exists(Path(self.out_path) / folder):
                shutil.rmtree(Path(self.out_path) / folder)
            os.mkdir(Path(self.out_path) / folder)

        if not os.path.exists(Path(self.in_path) / "mod.csv"):
            print(
                "ERROR: File {} not found.".format(str(Path(self.in_path) / "mod.csv"))
            )
            sys.exit()

    def optimize(self):
        """
        Optimize all known assets.
        """
        self.initialize_folders()
        self.csv.parse()

        # Optimize
        self.xmodel_container.add_items(self.csv["xmodel"])
        self.xmodel_container.optimize()
        self.xmodel_container.copy(self.out_path)

        self.material_container.add_items(self.csv["material"])
        self.material_container.add_items(self.xmodel_container.materials)
        self.material_container.optimize()
        self.material_container.copy(self.out_path)

        self.image_container.add_items(self.material_container.images)
        self.image_container.optimize()
        self.image_container.copy(self.out_path)

        print("\nDone!\n")
