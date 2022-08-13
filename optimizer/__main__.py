from pathlib import Path
from optimizer.assets import CSV, MaterialContainer, ImageContainer, XmodelContainer

import os
import sys

def parseCSV(in_path = None, out_path = None):
	"""
	Parse the main mod CSV and create hint txt files to be used 
	later with an asset container.
	"""
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
	"""
	Delete a file from a specified path.
	"""
	if os.path.exists(path):
		os.remove(path)


def checkPath(in_path = None, out_path = None):
	"""
	Setup all necessary folders and check if a mod CSV exists.
	"""
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
	"""
	Entry point of the program.
	"""
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
	"""
	Convert all known assets.
	"""
	# Create default folders.
	checkPath(in_path, out_path)

	Materials = MaterialContainer(in_path, out_path)
	XModels = XmodelContainer(in_path, out_path)
	Images = ImageContainer(in_path, out_path)

	# Delete any previous optimization.
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

	XModels.load_assets()
	XModels.move(XModels.out_path)
	XModels.optimize()

	print("""
#####################################
             Materials
#####################################
""")

	Materials.load_assets()
	Materials.move(Materials.out_path)
	Materials.optimize()

	print("""
#####################################
               Images
#####################################
""")

	Images.load_assets()
	Images.move(Images.out_path)

	print("\nDone!\n")


if __name__ == "__main__":
	main()
