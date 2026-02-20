import argparse

from pals import load
from pals.kinds import PlaceholderName
from pals.kinds.BeamLine import BeamLine
from pals.kinds.Drift import Drift
from pals.kinds.Lattice import Lattice
from pals.kinds.Quadrupole import Quadrupole


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
    assert isinstance(lattice.facility[0], Drift)
    assert lattice.facility[0].name == "drift1"
    assert isinstance(lattice.facility[1], Quadrupole)
    assert lattice.facility[1].name == "quad1"
    assert isinstance(lattice.facility[2], BeamLine)
    assert lattice.facility[2].name == "fodo_cell"
    assert isinstance(lattice.facility[3], BeamLine)
    assert lattice.facility[3].name == "fodo_channel"
    assert isinstance(lattice.facility[4], Lattice)
    assert lattice.facility[4].name == "fodo_lattice"
    assert isinstance(lattice.facility[5], PlaceholderName)


if __name__ == "__main__":
    main()
