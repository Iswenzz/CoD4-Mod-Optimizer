from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass

class CSV():

	@dataclass
	class AssetType:
		
		list: list
		parseName: str


	def __init__(self, path):

		self.csv_path = path
		self.csv_assets = {
			"xmodel": list(),
			"material": list(),
			"sound": list(),
			"weapon": list(),
			"xanim": list(),
			"menufile": list(),
			"fx": list(),
			"rawfile": list(),
			"localize": list(),
			"stringtable": list(),
		}
		self.csv_assets_tuple = [
			self.AssetType(self.csv_assets["xmodel"], "xmodel,"),
			self.AssetType(self.csv_assets["material"], "material,"),
			self.AssetType(self.csv_assets["sound"], "sound,"),
			self.AssetType(self.csv_assets["weapon"], "weapon,"),
			self.AssetType(self.csv_assets["xanim"], "xanim,"),
			self.AssetType(self.csv_assets["menufile"], "menufile,"),
			self.AssetType(self.csv_assets["fx"], "fx,"),
			self.AssetType(self.csv_assets["rawfile"], "rawfile,"),
			self.AssetType(self.csv_assets["localize"], "localize,"),
			self.AssetType(self.csv_assets["stringtable"], "stringtable,"),
		]

	
	def __getitem__(self, k):
		return self.csv_assets[k]


	def __setitem__(self, k, list):
		self.csv_assets[k] = list


	def __add__(self, other):

		s_info = self.csv_assets.values()
		o_info = other.csv_assets.values()

		for i in range(len(self.csv_assets)):
			for line in o_info[i]:
				s_info[i] += line
			
		return self


	def saveList(self, path, list):

		with open(Path(path), "w") as f:
			f.writelines(list)

	
	def save(self, path):
		
		with open(Path(path), "w") as f:
			for list in self.csv_assets.values():
				f.writelines(list)


	def parse(self, path, useAssetType = True):
		
		with open(Path(self.csv_path)) as csv_input:
			for line in csv_input:
				for asset in self.csv_assets_tuple:
					if asset.parseName in line:
						asset.list += line if useAssetType else line.replace(asset.parseName, "")
