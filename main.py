# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from material_asset import MaterialAsset
from image_asset import ImageAsset
from xmodel_asset import XmodelAsset

import os
import sys
import re
import shutil
import msvcrt
import time

def parseCSV():

	if not os.path.exists("out/csv/csv_material.txt"):
		with open("out/csv/csv_material.txt", "w"): pass
	if not os.path.exists("out/csv/csv_xmodel.txt"):
		with open("out/csv/csv_xmodel.txt", "w"): pass
	if not os.path.exists("out/csv/csv_material_all.txt"):
		with open("out/csv/csv_material_all.txt", "w"): pass

	csv_input = open("in/csv/mod.csv", "r")
	csv_material_output = open("out/csv/csv_material.txt", "w")
	csv_material_all_output = open("out/csv/csv_material_all.txt", "w")
	csv_xmodel_output = open("out/csv/csv_xmodel.txt", "w")

	with open("in/csv/mod.csv") as csv_input:
		for line in csv_input:

			if "xmodel," in line:
				csv_xmodel_output.write(line.replace("xmodel,", ""))
			elif "material," in line:
				csv_material_output.write(line.replace("material,", ""))

	for _, _, files in os.walk("in/materials", topdown = False):
		for name in files:
			csv_material_all_output.write(name + "\n")

	csv_input.close()
	csv_material_output.close()
	csv_material_all_output.close()
	csv_xmodel_output.close()


def delete(path):

	if os.path.exists(path):
		os.remove(path)

def main():

	Materials = MaterialAsset()
	XModels = XmodelAsset()
	Images = ImageAsset()

	print("Cleaning directories..")
	delete("out/csv/csv_material.txt")
	delete("out/csv/csv_material_all.txt")
	delete("out/csv/csv_xmodel.txt")
	delete("out/images_list.txt")
	delete("out/xmodel_material_list.txt")

	Materials.delete()
	XModels.delete()
	Images.delete()

	print("\nCreating new CSVs...")
	parseCSV()

	print("\n#####################################\n"
		+ "               XModels\n"
		+ "#####################################\n")

	XModels.loadAssets()
	XModels.move("in/xmodel")
	XModels.convert()

	print("\n#####################################\n"
		+ "              Materials\n"
		+ "#####################################\n")

	Materials.loadAssets()
	Materials.move("in/materials")
	Materials.convert()

	print("\n#####################################\n"
		+ "               Images\n"
		+ "#####################################\n")

	Images.loadAssets()
	Images.move("in/images")

	print("\nDone!\n")
	print("Press any key to continue...")
	# msvcrt.getch()

main()