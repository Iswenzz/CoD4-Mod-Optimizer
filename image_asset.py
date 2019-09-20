from iconvertableasset import IConvertableAsset
from pathlib import Path

import os
import re
import shutil

class ImageAsset(IConvertableAsset):

	csv_images_line = []

	def loadAssets(self):

		if os.path.exists("out/images_list.txt"):
			with open(u"out/images_list.txt") as c:
				self.csv_images_line = c.readlines()


	def move(self, path):

		for root, _, files in os.walk(u"in/images", topdown = False):
			for name in files:

				if name + "\n" in self.csv_images_line:
					f = os.path.join(root, name)
					print(name)
					shutil.copyfile(u"" + f, u"out/images/" + name)


	def convert(self):
		pass


	def delete(self):

		for root, _, files in os.walk("out/images", topdown = False):
			for name in files:
				f = os.path.join(root, name)
				delete(f)

def delete(path):

	if os.path.exists(path):
		os.remove(path)