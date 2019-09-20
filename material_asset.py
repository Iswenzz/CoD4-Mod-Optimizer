from iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil

class MaterialAsset(IConvertableAsset):

	csv_material_line = []
	csv_material_xmodel_line = []

	def cleanAssetList(self):

		outfile = []
		with open("out/images_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				outfile += line.replace("\n", ".iwi\n")
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def loadAssets(self):

		if os.path.exists("out/csv/csv_material.txt"):
			with open("out/csv/csv_material.txt") as c:
				self.csv_material_line = c.readlines()

		if os.path.exists("out/xmodel_material_list.txt"):
			with open("out/xmodel_material_list.txt") as c:
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

		if not os.path.exists("out/images_list.txt"):
			with open("out/images_list.txt", "w"): pass

		if os.path.exists("out/images_list.txt"):
			with open("out/images_list.txt", "a") as c:
				c.write(result)


	def move(self, path):

		for _, _, files in os.walk("in/materials", topdown = False):
			for name in files:

				if name + "\n" in self.csv_material_line:
					f = os.path.join(path, name)
					print(name)
					shutil.copyfile(f, Path("out/materials/") / name)

				elif name + "\n" in self.csv_material_xmodel_line:
					f = os.path.join(path, name)
					print(name)
					shutil.copyfile(f, Path("out/materials/") / name)


	def convert(self):

		for root, _, files in os.walk("out/materials", topdown = False):
			for name in files:
				f = os.path.join(root, name)
				self.findImages(f, name)
		
		self.cleanAssetList()


	def delete(self):

		for root, _, files in os.walk("out/materials", topdown = False):
			for name in files:
				f = os.path.join(root, name)
				delete(f)

def delete(path):

	if os.path.exists(path):
		os.remove(path)