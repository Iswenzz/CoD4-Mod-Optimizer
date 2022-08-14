from pathlib import Path
from typing import Dict, List
import os


class CSV():
	"""
	Represent a COD4 CSV file.
	"""
	csv_assets: Dict[str, List[str]] = {
		"xmodel": [],
		"material": [],
		"sound": [],
		"weapon": [],
		"xanim": [],
		"menufile": [],
		"fx": [],
		"localize": []
	}


	def __init__(self, csv_path: str):
		"""
		Initialize a new CSV object.
		"""
		self.csv_path = csv_path


	def __getitem__(self, name: str) -> List[str]:
		"""
		Indexer get asset type.
		"""
		return self.csv_assets[name]


	def __setitem__(self, name: str, assets: list):
		"""
		Indexer set asset type.
		"""
		self.csv_assets[name] = assets


	def parse(self):
		"""
		Parse the CSV assets.
		"""
		with open(Path(self.csv_path)) as f:
			# Parse lines
			for line in f:
				for name, list in self.csv_assets.items():
					delimiter = name + ","
					if line.startswith(delimiter):
						filename = line.strip().replace(delimiter, "")
						if filename not in list:
							list.append(filename)
