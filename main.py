# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pathlib import Path
from material_asset import MaterialAsset
from image_asset import ImageAsset
from xmodel_asset import XmodelAsset

import os
import sys
import re
import shutil
import msvcrt
import time

in_p = "in"
out_p = "out"

def parseCSV():

	if not os.path.exists(Path(out_p) / "csv/csv_material.txt"):
		with open(Path(out_p) / "csv/csv_material.txt", "w"): pass
	if not os.path.exists(Path(out_p) / "csv/csv_xmodel.txt"):
		with open(Path(out_p) / "csv/csv_xmodel.txt", "w"): pass
	if not os.path.exists(Path(out_p) / "csv/csv_material_all.txt"):
		with open(Path(out_p) / "csv/csv_material_all.txt", "w"): pass

	csv_input = open(Path(in_p) / "csv/mod.csv", "r")
	csv_material_output = open(Path(out_p) / "csv/csv_material.txt", "w")
	csv_material_all_output = open(Path(out_p) / "csv/csv_material_all.txt", "w")
	csv_xmodel_output = open(Path(out_p) / "csv/csv_xmodel.txt", "w")

	with open(Path(in_p) / "csv/mod.csv") as csv_input:
		for line in csv_input:

			if "xmodel," in line:
				csv_xmodel_output.write(line.replace("xmodel,", ""))
			elif "material," in line:
				csv_material_output.write(line.replace("material,", ""))

	for _, _, files in os.walk(Path(in_p) / "materials", topdown = False):
		for name in files:
			csv_material_all_output.write(name + "\n")

	csv_input.close()
	csv_material_output.close()
	csv_material_all_output.close()
	csv_xmodel_output.close()


def delete(path):

	if os.path.exists(path):
		os.remove(path)


def checkPath():

	if not os.path.exists(Path(in_p)):
		print("Folder doesn't exists: " + str(Path(in_p)))
		exit(-1)
	if not os.path.exists(Path(in_p) / "materials"):
		print("Folder doesn't exists: " + str(Path(in_p) / "materials"))
		exit(-1)
	if not os.path.exists(Path(in_p) / "xmodel"):
		print("Folder doesn't exists: " + str(Path(in_p) / "xmodel"))
		exit(-1)
	if not os.path.exists(Path(in_p) / "images"):
		print("Folder doesn't exists: " + str(Path(in_p) / "images"))
		exit(-1)

	if not os.path.exists(Path(out_p)):
		os.mkdir(Path(out_p))
	if not os.path.exists(Path(out_p) / "materials"):
		os.mkdir(Path(out_p) / "materials")
	if not os.path.exists(Path(out_p) / "xmodel"):
		os.mkdir(Path(out_p) / "xmodel")
	if not os.path.exists(Path(out_p) / "images"):
		os.mkdir(Path(out_p) / "images")
	if not os.path.exists(Path(out_p) / "csv"):
		os.mkdir(Path(out_p) / "csv")


def main():

	global in_p
	global out_p

	if len(sys.argv) == 3:
		in_p = sys.argv[1]
		out_p = sys.argv[2]
	else:
		print("Copyright (c) Iswenzz 2018-2019\n\n"
			+ "Usage: IWD Optimizer.exe \"C:/cod4/mod/name\" \"C:/cod4/mod/name/opti\"\n"
			+ "\t<input path> <output path> (default path is: EXE_DIR/in, EXE_DIR/out)\n\n")

	print("Input PATH: " + in_p + "\nOutput PATH: " + out_p + "\n")

	checkPath()

	Materials = MaterialAsset(in_p, out_p)
	XModels = XmodelAsset(in_p, out_p)
	Images = ImageAsset(in_p, out_p)

	delete(Path(in_p) / "csv/csv_material.txt")
	delete(Path(in_p) / "csv/csv_material_all.txt")
	delete(Path(in_p) / "csv/csv_xmodel.txt")
	delete(Path(in_p) / "images_list.txt")
	delete(Path(in_p) / "xmodel_material_list.txt")

	Materials.delete()
	XModels.delete()
	Images.delete()

	print("Parsing CSV...")
	
	parseCSV()

	print("\n#####################################\n"
		+ "               XModels\n"
		+ "#####################################\n")

	XModels.loadAssets()
	XModels.move(XModels.out_path)
	XModels.convert()

	print("\n#####################################\n"
		+ "              Materials\n"
		+ "#####################################\n")

	Materials.loadAssets()
	Materials.move(Materials.out_path)
	Materials.convert()

	print("\n#####################################\n"
		+ "               Images\n"
		+ "#####################################\n")

	Images.loadAssets()
	Images.move(Images.out_path)

	print("\nDone!\n")
	print("Press any key to continue...")
	# msvcrt.getch()

main()
