from optimizer.assets.containers.i_optimizable_container import IOptimizableContainer
from optimizer.assets.raw import Raw

from typing import List
from pathlib import Path
import re, os, shutil


class XModelContainer(IOptimizableContainer):
	"""
	Represent an asset container of CoD4 xmodel files.
	"""
	xmodels: List[str] = []
	materials: List[str] = []


	def __init__(self, raw: Raw):
		"""
		Initialize the XmodelContainer.
		"""
		self.raw = raw


	def add_items(self, items: List[str]):
		"""
		Add xmodels to the container to optimize.
		"""
		self.xmodels.extend(items)


	def find_materials(self, xmodel: str):
		"""
		Find all materials used by the xmodel.
		"""
		chars = r"A-Za-z0-9\-.,~_&$% "
		shortest_run = 1
		regexp = "[%s]{%d,}" % (chars, shortest_run)
		pattern = re.compile(regexp)

		xmodel_path = self.raw.get_file("xmodel", xmodel)
		if not os.path.exists(xmodel_path):
			return

		with open(xmodel_path, "rb") as binary_file:
			data = binary_file.read().decode("ansi")
			for material in pattern.findall(data):
				if material not in self.materials and material in self.raw.materials:
					self.materials.append(material)


	def optimize(self):
		"""
		Optimize all xmodels.
		"""
		for xmodel in self.xmodels:
			self.find_materials(xmodel)


	def copy(self, to_path: str):
		print()
		print("#####################################")
		print("               XModels               ")
		print("#####################################\n")

		for xmodel in self.xmodels:
			from_path = self.raw.get_file("xmodel", xmodel)
			if os.path.exists(from_path):
				print(xmodel)
				shutil.copy(from_path, Path(to_path) / "xmodel" / xmodel)
