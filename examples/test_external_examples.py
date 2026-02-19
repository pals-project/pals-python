import argparse

from pals import load


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the example file",
    )
    args = parser.parse_args()
    example_file = args.path
    # Parse and validate YAML data from file
    lattice = load(example_file)
    print(lattice.facility[0])


if __name__ == "__main__":
    main()
