from typing import Dict, List
from pathlib import Path


class CSV:

    assets: Dict[str, List[str]] = {
        "xmodel": [],
        "material": [],
        "image": [],
        "sound": [],
        "weapon": [],
        "xanim": [],
        "menufile": [],
        "fx": [],
        "localize": [],
    }

    def __init__(self, path: str):
        self.path = path
        self.parse()

    def __getitem__(self, name: str) -> List[str]:
        return self.assets[name]

    def __setitem__(self, name: str, assets: list):
        self.assets[name] = assets

    def parse(self):
        with open(Path(self.path), encoding="utf8") as csv_file:
            for line in csv_file:
                for name, array in self.assets.items():
                    delimiter = name + ","
                    if line.startswith(delimiter):
                        filename = line.strip().replace(delimiter, "")
                        if filename not in array:
                            array.append(filename)
