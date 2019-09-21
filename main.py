from pathlib import Path
from material_asset import MaterialAsset
from image_asset import ImageAsset
from xmodel_asset import XmodelAsset
from csv_file import CSV

import os
import sys

in_p = "in"
out_p = "out"

def parseCSV():

	if not os.path.exists(Path(out_p) / "csv/csv_material.txt"):
		with open(Path(out_p) / "csv/csv_material.txt", "w"): pass
	if not os.path.exists(Path(out_p) / "csv/csv_xmodel.txt"):
		with open(Path(out_p) / "csv/csv_xmodel.txt", "w"): pass
	if not os.path.exists(Path(out_p) / "csv/csv_material_all.txt"):
		with open(Path(out_p) / "csv/csv_material_all.txt", "w"): pass

	csv_input = CSV(Path(in_p) / "mod.csv")
	csv_input.parse(csv_input.csv_path, useAssetType = False)

	with open(Path(out_p) / "csv/csv_material.txt", "w") as f:
		f.writelines(csv_input.csv_assets["material"])
	with open(Path(out_p) / "csv/csv_xmodel.txt", "w") as f:
		f.writelines(csv_input.csv_assets["xmodel"])

	with open(Path(out_p) / "csv/csv_material_all.txt", "w") as f:
		for _, _, files in os.walk(Path(in_p) / "materials", topdown = False):
			for name in files:
				f.write(name + "\n")


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
	if not os.path.exists(Path(in_p) / "mod.csv"):
		print("mod.csv doesn't exists: " + str(Path(in_p) / "mod.csv"))
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

	convert()


def convert(in_path = None, out_path = None):

	if in_path is not None:
		global in_p
		in_p = in_path
	if out_path is not None:
		global out_p
		out_p = out_path

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


if __name__ == "__main__":
	main()
