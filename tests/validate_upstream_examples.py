"""Utility script to validate upstream PALS example files.

This script is not run by pytest and is intended to be used as a standalone script.
Run it from the repository root like:

    python tests/validate_upstream_examples.py --path /path/to/example.pals.yaml

Before running, download the desired upstream PALS example files from pals-project/pals/examples.
"""

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
    # The following assertions are based on the upstream PALS example file
    # fodo.pals.yaml from pals-project/pals/examples
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
