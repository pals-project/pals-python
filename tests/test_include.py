"""Tests for resolving `include` entries while loading files.

The documents used here live under tests/pals_files/include and
tests/pals_files/lattice_use, one directory per scenario.
"""

import pathlib

import pytest

import pals

PALS_FILES = pathlib.Path(__file__).parent / "pals_files"
INCLUDE = PALS_FILES / "include"
LATTICE_USE = PALS_FILES / "lattice_use"


def test_include():
    """Includes splice into the root node and the facility list."""
    main_file = str(INCLUDE / "main.pals.yaml")

    lattice = pals.Lattice.from_file(main_file)
    assert lattice.name == "fodo_lattice"
    assert lattice.branches[0] == "fodo_cell"

    data = pals.PALSroot.from_file(main_file)
    # From the root-level include of globals.subpals.yaml, with the
    # unmodeled key preserved.
    assert data.version == 1.0
    assert data.notes == ["included note"]
    assert data.my_extension_data == "kept"
    assert not hasattr(data, "include")

    # sub/quads.subpals.yaml spliced in quad1 and drift2, and its own
    # include (resolved relative to sub/) spliced in quad2.
    names = [elem.name for elem in data.facility]
    assert names == [
        "drift1",
        "quad1",
        "drift2",
        "quad2",
        "fodo_cell",
        "fodo_lattice",
        "fodo_lattice",
    ]
    assert isinstance(data.facility[3], pals.Quadrupole)
    assert data.facility[3].MagneticMultipoleP.Bn1 == -1.0


def test_nested_include():
    """A chain of includes resolves through each file; local keys win."""
    data = pals.functions.load_file_to_dict(str(INCLUDE / "nested/root.pals.yaml"))

    assert data["root"]["middle"] == "val"
    assert data["root"]["leaf"] == "val"
    # The including file's own entry wins over the included one.
    assert data["root"]["shared"] == "local"
    assert "include" not in data["root"]


def test_include_element_parameters():
    """The standard's element-level include example: a parameter group file."""
    data = pals.functions.load_file_to_dict(str(INCLUDE / "element/q01.pals.yaml"))

    assert data["Q01"] == {
        "kind": "Quadrupole",
        "MagneticMultipoleP": {"Kn3L": 0.3},
    }


def test_include_structure_mismatch():
    """Including a sequence at a mapping level is a structural error."""
    with pytest.raises(TypeError, match="mapping level"):
        pals.functions.load_file_to_dict(str(INCLUDE / "mismatch/q01.pals.yaml"))


def test_circular_include():
    """An include cycle is reported instead of recursing forever."""
    with pytest.raises(RuntimeError, match="circular include"):
        pals.functions.load_file_to_dict(str(INCLUDE / "circular/a.pals.yaml"))


def test_lattice_from_full_document_use():
    """Per the use statement, the last lattice is instantiated unless a
    `use` entry selects another."""
    lattice = pals.Lattice.from_file(str(LATTICE_USE / "no_use.pals.yaml"))
    assert lattice.name == "lat2"

    lattice = pals.Lattice.from_file(str(LATTICE_USE / "with_use.pals.yaml"))
    assert lattice.name == "lat1"

    with pytest.raises(ValueError, match="does not define a Lattice"):
        pals.Lattice.from_file(str(LATTICE_USE / "no_lattice.pals.yaml"))
