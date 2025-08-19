from typing import Dict, List
from pathlib import Path
from os import walk


class Raw:
    """
    Represent the raw folder.
    """

    registry: Dict[str, List[str]] = {
        "xmodel": ["xmodel"],
        "material": ["materials"],
        "sound": ["sound"],
        "weapon": ["weapons"],
        "xanim": ["xanim"],
        "menufile": ["ui", "ui_mp"],
        "fx": ["fx"],
        "localize": ["english/localizedstrings"],
        "image": ["images"],
    }

    path: str
    images: List[str] = []
    materials: List[str] = []
    xmodels: List[str] = []

    @staticmethod
    def initialize(path: str):
        """
        Initialize the raw folder.
        """
        Raw.path = path
        Raw.images = Raw.files("image")
        Raw.materials = Raw.files("material")
        Raw.xmodels = Raw.files("xmodel")

    @staticmethod
    def file(asset: str, filename: str) -> str:
        """
        Get a file.
        """
        return Path(Raw.path) / asset / filename

    @staticmethod
    def files(asset: str) -> List[str]:
        """
        Get all files.
        """
        array = []
        for folder in Raw.registry[asset]:
            for _, _, files in walk(Path(Raw.path) / folder, topdown=False):
                array.extend(files)
        return array
