from pathlib import Path
from assets import CSV, MaterialAsset, ImageAsset, XmodelAsset

import os
import sys

def parseCSV(in_path = None, out_path = None):

	if not os.path.exists(Path(out_path) / "csv/csv_material.txt"):
		with open(Path(out_path) / "csv/csv_material.txt", "w"):
			pass
	if not os.path.exists(Path(out_path) / "csv/csv_xmodel.txt"):
		with open(Path(out_path) / "csv/csv_xmodel.txt", "w"):
			pass
	if not os.path.exists(Path(out_path) / "csv/csv_material_all.txt"):
		with open(Path(out_path) / "csv/csv_material_all.txt", "w"):
			pass

	csv_input = CSV(Path(in_path) / "mod.csv")
	csv_input.parse(csv_input.csv_path, useAssetType = False)

	with open(Path(out_path) / "csv/csv_material.txt", "w") as f:
		f.writelines(csv_input.csv_assets["material"])
	with open(Path(out_path) / "csv/csv_xmodel.txt", "w") as f:
		f.writelines(csv_input.csv_assets["xmodel"])

	with open(Path(out_path) / "csv/csv_material_all.txt", "w") as f:
		for _, _, files in os.walk(Path(in_path) / "materials", topdown = False):
			for name in files:
				f.write(name + "\n")


def delete(path):

	if os.path.exists(path):
		os.remove(path)


def checkPath(in_path = None, out_path = None):

	in_check = ["materials", "xmodel", "images"]
	out_check = ["materials", "xmodel", "images", "csv"]

	if not os.path.exists(in_path):
		os.mkdir(in_path)
	if not os.path.exists(out_path):
		os.mkdir(out_path)

	for f in in_check:
		if not os.path.exists(Path(in_path) / f):
			os.mkdir(Path(in_path) / f)

	for f in out_check:
		if not os.path.exists(Path(out_path) / f):
			os.mkdir(Path(out_path) / f)

	if not os.path.exists(Path(in_path) / "mod.csv"):
		print("ERROR: File " + str(Path(in_path) / "mod.csv") + " not found.")
		sys.exit()


def main():

	in_p = "in"
	out_p = "out"

	if len(sys.argv) == 3:
		in_p = sys.argv[1]
		out_p = sys.argv[2]
	else:
		print("""
Copyright (c) Iswenzz 2018-2020

Usage: IWD Optimizer.exe "C:/cod4/mod/name" "C:/cod4/mod/name/opti"
	<input path> <output path> (default path is: EXE_DIR/in, EXE_DIR/out)\n
""")

	print("Input PATH: " + in_p + "\nOutput PATH: " + out_p + "\n")

	convert(in_p, out_p)


def convert(in_path = None, out_path = None):

	checkPath(in_path, out_path)

	Materials = MaterialAsset(in_path, out_path)
	XModels = XmodelAsset(in_path, out_path)
	Images = ImageAsset(in_path, out_path)

	delete(Path(out_path) / "csv/csv_material.txt")
	delete(Path(out_path) / "csv/csv_material_all.txt")
	delete(Path(out_path) / "csv/csv_xmodel.txt")
	delete(Path(out_path) / "images_list.txt")
	delete(Path(out_path) / "xmodel_material_list.txt")

	Materials.delete()
	XModels.delete()
	Images.delete()

	print("Parsing CSV...")

	parseCSV(in_path, out_path)

	print("""
#####################################
              XModels
#####################################
""")

	XModels.loadAssets()
	XModels.move(XModels.out_path)
	XModels.convert()

	print("""
#####################################
             Materials
#####################################
""")

	Materials.loadAssets()
	Materials.move(Materials.out_path)
	Materials.convert()

	print("""
#####################################
               Images
#####################################
""")

	Images.loadAssets()
	Images.move(Images.out_path)

	print("\nDone!\n")


if __name__ == "__main__":
	main()
