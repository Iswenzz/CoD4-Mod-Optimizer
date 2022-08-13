from optimizer.assets.i_optimizable_container import IOptimizableContainer
from pathlib import Path

import os
import re
import shutil

class XmodelContainer(IOptimizableContainer):
	"""
	Represent an asset container of CoD4 xmodel files.
	"""

	def __init__(self, in_path, out_path):
		"""
		Initialize a new XmodelContainer object.

		inp: input xmodel folder path.
		outp: output xmodel folder path.
		"""
		self.csv_xmodel_lines = []
		self.in_path = in_path
		self.out_path = out_path


	def clean_asset_list(self):
		"""
		Create a new CSV hint file with the optimized assets.
		"""
		if os.path.exists(Path(self.out_path) / "csv/csv_material_all.txt"):
			with open(Path(self.out_path) / "csv/csv_material_all.txt") as c:
				csv_material_all_line = c.readlines()

		outfile = []
		with open(Path(self.out_path) / "xmodel_material_list.txt", "r+") as f:
			for line in f:
				if not line.strip():
					continue
				if line in csv_material_all_line and line not in outfile:
					outfile.append(line)
			f.seek(0)
			f.writelines(outfile)
			f.truncate()


	def load_assets(self):
		"""
		Load all xmodel from the CSV Hint file.
		"""
		if os.path.exists(Path(self.out_path) / "csv/csv_xmodel.txt"):
			with open(Path(self.out_path) / "csv/csv_xmodel.txt") as c:
				self.csv_xmodel_lines = c.readlines()


	def find_xmodels(self, path):
		"""
		Find all materials used by the xmodel.
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

		if not os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt", "w"): 
				pass

		if os.path.exists(Path(self.out_path) / "xmodel_material_list.txt"):
			with open(Path(self.out_path) / "xmodel_material_list.txt", "a") as c:
				c.write(result)
	

	def move(self, path):
		"""
		Move all xmodel to a specified path.
		"""
		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "xmodel", topdown = False):
			for name in files:

				if name + "\n" in self.csv_xmodel_lines:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("xmodel/" + name))


	def optimize(self):
		"""
		Optimize all xmodel.
		"""
		for root, _, files in os.walk(Path(self.out_path) / "xmodel", topdown = False):
			for name in files:
				f = Path(root) / name
				self.find_xmodels(f)

		self.clean_asset_list()

	
	def delete(self):
		"""
		Delete all xmodel.
		"""
		for root, _, files in os.walk(Path(self.out_path) / "xmodel", topdown = False):
			for name in files:
				f = Path(root) / name
				if os.path.exists(f):
					os.remove(f)
