"""Validate the standard PALS example files from pals-project/pals/examples.

Every *.pals.yaml file under --root is discovered and must be readable with
pals.load(). *.subpals.yaml files are exempt: per the standard's notation
section they are sub-level include fragments, spliced into (and read through)
the file that includes them.

A few files additionally get structural spot-checks (see SPOT_CHECKS), because
loading without an error is not by itself evidence that a file was read
correctly: a facility entry that matches no element still lands somewhere in
the element union.

Files this implementation cannot read yet are recorded in the known-failures
list (tests/standard_examples_known_failures.txt): a failure of a listed file
is expected, and a listed file that starts to load is reported so the list
shrinks as support lands.

This script is not run by pytest; the standard_examples workflow runs it
against a checkout of the standard, pinned to the commit named in
tests/standard_examples_git_reference.txt. Run it locally, from the repository root:

    python tests/validate_standard_examples.py \
        --root /path/to/pals/examples \
        --known-failures tests/standard_examples_known_failures.txt
"""

import argparse
import pathlib
import sys

import pals


def check_fodo(root):
    """Structural spot-checks of the introductory example fodo.pals.yaml."""
    from pals.kinds import PlaceholderName
    from pals.kinds.BeamLine import BeamLine
    from pals.kinds.Drift import Drift
    from pals.kinds.Lattice import Lattice
    from pals.kinds.Quadrupole import Quadrupole

    assert isinstance(root.facility[0], Drift)
    assert root.facility[0].name == "drift1"
    assert isinstance(root.facility[1], Quadrupole)
    assert root.facility[1].name == "quad1"
    assert isinstance(root.facility[2], BeamLine)
    assert root.facility[2].name == "fodo_cell"
    assert isinstance(root.facility[3], BeamLine)
    assert root.facility[3].name == "fodo_channel"
    assert isinstance(root.facility[4], Lattice)
    assert root.facility[4].name == "fodo_lattice"
    assert isinstance(root.facility[5], PlaceholderName)


def check_sets_compact(root):
    """Structural spot-checks of unit_tests/sets/sets_compact.pals.yaml.

    A file that merely loads is not evidence that it was read correctly: a
    facility entry that matches no element still lands somewhere in the element
    union. This asserts the compact `sets` form is read as the command it is.
    """
    from pals.commands import SetsCommand

    commands = [item for item in root.facility if isinstance(item, SetsCommand)]
    assert len(commands) == 1
    assert [(pair.parameter, pair.value) for pair in commands[0].sets] == [
        ("Q1>MagneticMultipoleP.Kn1L", 0.25),
        ("D1>length", "2 * 1.5"),
    ]


# Files that get structural spot-checks beyond loading, by root-relative path.
SPOT_CHECKS = {
    "fodo.pals.yaml": check_fodo,
    "unit_tests/sets/sets_compact.pals.yaml": check_sets_compact,
}


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

    # Track every unexpected result for the final exit status.
    failures = 0
    seen = set()
    files = sorted(root.rglob("*.pals.yaml"))
    for path in files:
        rel = path.relative_to(root).as_posix()
        seen.add(rel)
        error = None
        # Capture load errors so expected failures can be distinguished.
        try:
            loaded = pals.load(str(path))
            spot_check = SPOT_CHECKS.get(rel)
            if spot_check is not None:
                spot_check(loaded)
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

    # Flag stale entries in the known-failures list.
    for rel in sorted(known - seen):
        print(f"FAIL   {rel}")
        print("       in the known-failures list, but not found under --root")
        failures += 1

    print(f"{len(files)} files checked, {failures} unexpected results")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
