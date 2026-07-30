"""Validate the standard PALS example files from pals-project/pals/examples.

Every *.pals.yaml file under --root is discovered and must be readable with
pals.load(). *.subpals.yaml files are exempt: per the standard's notation
section they are sub-level include fragments, spliced into (and read through)
the file that includes them.

Files this implementation cannot read yet are recorded in the known-failures
list (tests/standard_examples_known_failures.txt): a failure of a listed file
is expected, and a listed file that starts to load is reported so the list
shrinks as support lands.

This script is not run by pytest; the standard_examples workflow runs it
against a checkout of the standard, pinned to the commit named in
tests/pals_standard_ref.txt. Run it locally, from the repository root:

    python tests/validate_standard_examples.py \
        --root /path/to/pals/examples \
        --known-failures tests/standard_examples_known_failures.txt
"""

import argparse
import pathlib
import sys

import pals


def check_fodo(lattice):
    """Structural spot-checks of the introductory example fodo.pals.yaml."""
    from pals.kinds import PlaceholderName
    from pals.kinds.BeamLine import BeamLine
    from pals.kinds.Drift import Drift
    from pals.kinds.Lattice import Lattice
    from pals.kinds.Quadrupole import Quadrupole

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


def read_known_failures(path):
    """The known-failures list: one root-relative path per line, # comments."""
    known = set()
    for line in pathlib.Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            known.add(line)
    return known


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        required=True,
        help="Path to the standard's examples directory",
    )
    parser.add_argument(
        "--known-failures",
        required=True,
        help="Path to the known-failures list",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    known = read_known_failures(args.known_failures)

    failures = 0
    seen = set()
    files = sorted(root.rglob("*.pals.yaml"))
    for path in files:
        rel = path.relative_to(root).as_posix()
        seen.add(rel)
        error = None
        try:
            lattice = pals.load(str(path))
            if rel == "fodo.pals.yaml":
                check_fodo(lattice)
        except Exception as e:  # noqa: BLE001 -- any reader failure counts
            error = e
        if rel in known:
            if error is None:
                print(f"XPASS  {rel}")
                print("       loads now: remove it from the known-failures list")
                failures += 1
            else:
                print(f"XFAIL  {rel}")
        elif error is None:
            print(f"PASS   {rel}")
        else:
            print(f"FAIL   {rel}")
            message = f"{type(error).__name__}: {error}"
            for detail in message.splitlines()[:3]:
                print(f"       {detail}")
            failures += 1

    # A listed file that no longer exists means the corpus moved on and the
    # list still describes it.
    for rel in sorted(known - seen):
        print(f"FAIL   {rel}")
        print("       in the known-failures list, but not found under --root")
        failures += 1

    print(f"{len(files)} files checked, {failures} unexpected results")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
