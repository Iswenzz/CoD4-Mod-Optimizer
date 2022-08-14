from optimizer.assets.asset import assets_directories

from pathlib import Path
from typing import List
import os


class Raw:
    """
    Represent the raw folder.
    """

    def __init__(self, path: str):
        """
        Initialize the Raw folder instance.
        """
        self.path = path
        self.images = self.get_assets("image")
        self.materials = self.get_assets("material")
        self.xmodels = self.get_assets("xmodel")

    def get_file(self, asset: str, filename: str) -> str:
        """
        Get a specific file.
        """
        return Path(self.path) / asset / filename

    def get_assets(self, asset: str) -> List[str]:
        """
        Get all assets.
        """
        list = []
        for folder in assets_directories[asset]:
            for root, _, files in os.walk(Path(self.path) / folder, topdown=False):
                list.extend(files)
        return list
