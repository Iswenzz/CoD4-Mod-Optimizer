from optimizer.assets.containers.i_optimizable_container import IOptimizableContainer
from optimizer.assets.raw import Raw

from typing import List
from pathlib import Path
import re, os, shutil


class MaterialContainer(IOptimizableContainer):
	"""
	Represent an asset container of CoD4 material files.
	"""
	materials: List[str] = []
	images: List[str] = []


	def __init__(self, raw: Raw):
		"""
		Initialize the MaterialContainer.
		"""
		self.raw = raw


	def add_items(self, items: List[str]):
		"""
		Add materials to the container to optimize.
		"""
		self.materials.extend(items)


	def find_images(self, material: str):
		"""
		Find all images used by the material.
		"""
		chars = r"A-Za-z0-9\-.,~_&$% "
		shortest_run = 1
		regexp = "[%s]{%d,}" % (chars, shortest_run)
		pattern = re.compile(regexp)

		material_path = self.raw.get_file("materials", material)
		if not os.path.exists(material_path):
			return

		with open(material_path, "rb") as binary_file:
			data = binary_file.read().decode("ansi")
			for image in pattern.findall(data):
				if image not in self.images and image + ".iwi" in self.raw.images:
					self.images.append(image)


	def optimize(self):
		"""
		Optimize all materials.
		"""
		for material in self.materials:
			self.find_images(material)


	def copy(self, to_path: str):
		print()
		print("#####################################")
		print("              Materials              ")
		print("#####################################\n")

		for material in self.materials:
			from_path = self.raw.get_file("materials", material)
			from_path_properties = self.raw.get_file("material_properties", material)
			if os.path.exists(from_path):
				print(material)
				shutil.copy(from_path, Path(to_path) / "materials" / material)
			if os.path.exists(from_path_properties):
				shutil.copy(from_path_properties, Path(to_path) / "material_properties" / material)
