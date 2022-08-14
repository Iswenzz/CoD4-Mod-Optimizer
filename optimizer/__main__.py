from container import Container
import sys


help_message = """CoD4 Mod Optimizer (c) Iswenzz 2018-2022\n
Usage: mod_optimizer.exe <input path> <output path>
"""


def main():
    """
    Entry point of the program.
    """
    input_path = "in"
    output_path = "out"

    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        print(help_message)

    print("Input: {} \nOutput: {}\n".format(input_path, output_path))
    Container(input_path, output_path)


if __name__ == "__main__":
    main()
