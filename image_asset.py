from iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil

class ImageAsset(IConvertableAsset):

	def __init__(self, inp, outp):

		self.csv_images_line = []
		self.in_path = inp
		self.out_path = outp


	def loadAssets(self):

		if os.path.exists(Path(self.out_path) / "images_list.txt"):
			with open(Path(self.out_path) / "images_list.txt") as c:
				self.csv_images_line = c.readlines()


	def move(self, path):

		self.out_path = path

		for root, _, files in os.walk(Path(self.in_path) / "images", topdown = False):
			for name in files:

				if name + "\n" in self.csv_images_line:
					f = Path(root) / name
					print(name)
					shutil.copyfile(f, Path(self.out_path) / Path("images/" + name))


	def convert(self):
		pass


	def delete(self):

		for root, _, files in os.walk(Path(self.out_path) / "images", topdown = False):
			for name in files:
				f = Path(root) / name
				delete(f)


def delete(path):

	if os.path.exists(path):
		os.remove(path)
