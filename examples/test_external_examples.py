import argparse
import yaml

from pals import BeamLine


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
    # Read YAML data from file
    with open(example_file, "r") as file:
        data = yaml.safe_load(file)
    # Parse and validate YAML data
    print(f"Parsing data from {example_file}...")
    BeamLine(**data)


if __name__ == "__main__":
    main()
