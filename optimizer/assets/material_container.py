from optimizer.assets.i_optimizable_container import IOptimizableContainer
from pathlib import Path

import os
import re
import shutil

class MaterialContainer(IOptimizableContainer):
	"""
	Represent an asset container of CoD4 material files.
	"""

	def __init__(self, in_path, out_path):
		"""
		Initialize a new MaterialContainer object.

		inp: input material folder path.
		outp: output material folder path.
		"""
		self.csv_material_lines = []
		self.csv_material_xmodel_lines = []
		self.in_path = in_path
		self.out_path = out_path


	def clean_asset_list(self):
		"""
		Create a new CSV hint file with the optimized assets.
		"""
		outfile = []
		with open(Path(self.out_path) / "images_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				if line.replace("\n", ".iwi\n") not in outfile:
					outfile.append(line.replace("\n", ".iwi\n"))
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def load_assets(self):
		"""
		Load all material from the CSV Hint file.
		"""
		if os.path.exists(Path(self.out_path) / "csv/csv_material.txt"):
			with open(Path(self.out_path) / "csv/csv_material.txt") as c:
				self.csv_material_lines = c.readlines()

		if os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt") as c:
				self.csv_material_xmodel_lines = c.readlines()


	def find_images(self, path):
		"""
		Find all images used by the material.
		"""
		result = ""
		chars = r"A-Za-z0-9\-.,~_&$% "
		shortest_run = 1

		regexp = '[%s]{%d,}' % (chars, shortest_run)
		pattern = re.compile(regexp)

		with open(path, "rb") as binary_file:
			data = binary_file.read().decode("ansi")
			for _str in pattern.findall(data):
				result += _str + "\n"

		if not os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt", "w"): 
				pass

		if os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt", "a") as c:
				c.write(result)


	def move(self, path):
		"""
		Move all material to a specified path.
		"""
		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "materials", topdown = False):
			for name in files:

				if name + "\n" in self.csv_material_lines:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("materials/" + name))

				elif name + "\n" in self.csv_material_xmodel_lines:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("materials/" + name))


	def optimize(self):
		"""
		Optimize all material.
		"""
		for root, _, files in os.walk(Path(self.out_path) / "materials", topdown = False):
			for name in files:
				f = Path(root) / name
				self.find_images(f)
		
		self.clean_asset_list()


	def delete(self):
		"""
		Delete all material.
		"""
		for root, _, files in os.walk(Path(self.out_path) / "materials", topdown = False):
			for name in files:
				f = Path(root) / name
				if os.path.exists(f):
					os.remove(f)
