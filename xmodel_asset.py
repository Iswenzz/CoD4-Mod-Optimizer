from iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil

class XmodelAsset(IConvertableAsset):

	csv_xmodel_line = []

	def cleanAssetList(self):

		if os.path.exists("out/csv/csv_material_all.txt"):
			with open("out/csv/csv_material_all.txt") as c:
				csv_material_all_line = c.readlines()

		outfile = []
		with open("out/xmodel_material_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				if line in csv_material_all_line:
					outfile += line
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def loadAssets(self):

		if os.path.exists("out/csv/csv_xmodel.txt"):
			with open("out/csv/csv_xmodel.txt") as c:
				self.csv_xmodel_line = c.readlines()


	def findXmodels(self, path, name):

		result = ""
		valid_string = ""
		data = ""

		valid = "abcdefghijklmnopqrstuvwxyz_~-$0123456789."

		with open(path, "rb") as binary_file:
			data = binary_file.read()

		result = data.replace(b"\x00", b".")
		result = result.decode("ansi")

		for char in result:
			if char in valid:
				valid_string += char

		result = re.sub(r".*" + name, "", valid_string)
		result = result.replace(".", " ")
		result = result.replace(" ", "\n")

		if not os.path.exists("out/xmodel_material_list.txt"):
			with open("out/xmodel_material_list.txt", "w"): pass

		if os.path.exists("out/xmodel_material_list.txt"):
			with open("out/xmodel_material_list.txt", "a") as c:
				c.write(result)
	

	def move(self, path):

		for root, _, files in os.walk("in/xmodel", topdown = False):
			for name in files:

				if name + "\n" in self.csv_xmodel_line:
					f = os.path.join(root, name)
					print(name)
					shutil.copyfile(f, Path("out/xmodel/") / name)


	def convert(self):

		for root, _, files in os.walk("out/xmodel", topdown = False):
			for name in files:
				f = os.path.join(root, name)
				self.findXmodels(f, name)

		self.cleanAssetList()

	
	def delete(self):

		for root, _, files in os.walk("out/xmodel", topdown = False):
			for name in files:
				f = os.path.join(root, name)
				delete(f)

def delete(path):

	if os.path.exists(path):
		os.remove(path)