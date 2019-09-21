from iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil

class MaterialAsset(IConvertableAsset):

	def __init__(self, inp, outp):

		self.csv_material_line = []
		self.csv_material_xmodel_line = []
		self.in_path = inp
		self.out_path = outp


	def cleanAssetList(self):

		outfile = []
		with open(Path(self.out_path) / "images_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				outfile += line.replace("\n", ".iwi\n")
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def loadAssets(self):

		if os.path.exists(Path(self.out_path) / "csv/csv_material.txt"):
			with open(Path(self.out_path) / "csv/csv_material.txt") as c:
				self.csv_material_line = c.readlines()

		if os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt") as c:
				self.csv_material_xmodel_line = c.readlines()


	def findImages(self, path, name):

		result = ""
		file_string = ""
		valid = "abcdefghijklmnopqrstuvwxyz_~-$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ&"

		with open(path, "r", encoding = "Latin-1") as f:
			for line in f:
				file_string += line

		valid_string = ""
		for char in file_string:
			if char in valid:
				valid_string += char

		result = valid_string.replace(name, "DELETE_THIS", 1)
		result = result.replace("2d", "DELETE_THIS", 1)
		result = re.sub(r".*DELETE_THIS", " ", result)
		result = re.sub(r"envMapParmscolorTint*", " ", result, 1)
		result = result.replace("colorMap", "")
		result = result.replace("normalMap", " ")
		result = result.replace("specularMap", " ")
		result = result.replace("detailMap", " ")
		result = result.replace(" ", "\n")
		result = result.replace("identitynormalmapcolorTint", "")
		result = result.replace("dynamicFoliageSunDiffuseMinMax", "")
		result = result.replace("colorTint", "")
		result = result.replace("detailScale", "")

		if not os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt", "w"): pass

		if os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt", "a") as c:
				c.write(result)


	def move(self, path):

		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "materials", topdown = False):
			for name in files:

				if name + "\n" in self.csv_material_line:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("materials/" + name))

				elif name + "\n" in self.csv_material_xmodel_line:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("materials/" + name))


	def convert(self):

		for root, _, files in os.walk(Path(self.out_path) / "materials", topdown = False):
			for name in files:
				f = Path(root) / name
				self.findImages(f, name)
		
		self.cleanAssetList()


	def delete(self):

		for root, _, files in os.walk(Path(self.out_path) / "materials", topdown = False):
			for name in files:
				f = Path(root) / name
				delete(f)


def delete(path):

	if os.path.exists(path):
		os.remove(path)
