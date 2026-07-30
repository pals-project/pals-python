"""Tests for resolving `include` entries while loading files."""

import textwrap

import pytest

import pals


def write(path, text):
    """Write a dedented YAML document, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text))
    return path


def test_include(tmp_path):
    """Includes splice into the root node and the facility list."""
    main_file = write(
        tmp_path / "main.pals.yaml",
        """\
        PALS:
          include: "globals.subpals.yaml"
          facility:
            - drift1:
                kind: Drift
                length: 0.25

            - include: "sub/quads.subpals.yaml"

            - fodo_cell:
                kind: BeamLine
                line:
                  - drift1
                  - quad1
                  - drift2
                  - quad2
                  - drift1

            - fodo_lattice:
                kind: Lattice
                branches:
                  - fodo_cell

            - use: fodo_lattice
        """,
    )
    # Root-level include: version and notes per the standard's example, plus
    # an unmodeled key that must be preserved.
    write(
        tmp_path / "globals.subpals.yaml",
        """\
        version: 1.0
        notes:
          - "included note"
        my_extension_data: "kept"
        """,
    )
    # Facility-level include, itself including a file relative to its own
    # directory (not the directory of the main file).
    write(
        tmp_path / "sub" / "quads.subpals.yaml",
        """\
        - quad1:
            kind: Quadrupole
            MagneticMultipoleP:
              Bn1: 1.0
            length: 1.0

        - drift2:
            kind: Drift
            length: 0.5

        - include: "../parts/extra.subpals.yaml"
        """,
    )
    write(
        tmp_path / "parts" / "extra.subpals.yaml",
        """\
        - quad2:
            kind: Quadrupole
            MagneticMultipoleP:
              Bn1: -1.0
            length: 1.0
        """,
    )

    lattice = pals.Lattice.from_file(main_file)
    assert lattice.name == "fodo_lattice"
    assert lattice.branches[0] == "fodo_cell"

    data = pals.PALSroot.from_file(main_file)
    assert data.version == 1.0
    assert data.notes == ["included note"]
    assert data.my_extension_data == "kept"
    assert not hasattr(data, "include")

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


def test_nested_include(tmp_path):
    """A chain of includes resolves through each file; local keys win."""
    root_file = write(
        tmp_path / "root.pals.yaml",
        """\
        root:
          include: "middle.subpals.yaml"
        """,
    )
    write(
        tmp_path / "middle.subpals.yaml",
        """\
        middle: val
        shared: local
        include: "leaf.subpals.yaml"
        """,
    )
    write(
        tmp_path / "leaf.subpals.yaml",
        """\
        leaf: val
        shared: included
        """,
    )

    data = pals.functions.load_file_to_dict(str(root_file))

    assert data["root"]["middle"] == "val"
    assert data["root"]["leaf"] == "val"
    # The including file's own entry wins over the included one.
    assert data["root"]["shared"] == "local"
    assert "include" not in data["root"]


def test_include_element_parameters(tmp_path):
    """The standard's element-level include example: a parameter group file."""
    main_file = write(
        tmp_path / "element.pals.yaml",
        """\
        Q01:
          kind: Quadrupole
          include: "include-Q-params.subpals.yaml"
        """,
    )
    write(
        tmp_path / "include-Q-params.subpals.yaml",
        """\
        MagneticMultipoleP:
          Kn3L: 0.3
        """,
    )

    data = pals.functions.load_file_to_dict(str(main_file))
    assert data["Q01"] == {
        "kind": "Quadrupole",
        "MagneticMultipoleP": {"Kn3L": 0.3},
    }


def test_include_structure_mismatch(tmp_path):
    """Including a sequence at a mapping level is a structural error."""
    main_file = write(
        tmp_path / "element.pals.yaml",
        """\
        Q01:
          kind: Quadrupole
          include: "elements.subpals.yaml"
        """,
    )
    write(
        tmp_path / "elements.subpals.yaml",
        """\
        - a:
            kind: Drift
        """,
    )

    with pytest.raises(TypeError, match="mapping level"):
        pals.functions.load_file_to_dict(str(main_file))


def test_circular_include(tmp_path):
    """An include cycle is reported instead of recursing forever."""
    a_file = write(
        tmp_path / "a.pals.yaml",
        """\
        PALS:
          include: "b.subpals.yaml"
        """,
    )
    write(
        tmp_path / "b.subpals.yaml",
        """\
        include: "a.pals.yaml"
        """,
    )

    with pytest.raises(RuntimeError, match="circular include"):
        pals.functions.load_file_to_dict(str(a_file))


def test_lattice_from_full_document_use(tmp_path):
    """Per the use statement, the last lattice is instantiated unless a
    `use` entry selects another."""
    content = """\
    PALS:
      facility:
        - line1:
            kind: BeamLine
            line:
              - m1:
                  kind: Marker
        - lat1:
            kind: Lattice
            branches:
              - line1
        - lat2:
            kind: Lattice
            branches:
              - line1
    """
    no_use = write(tmp_path / "no_use.pals.yaml", content)
    assert pals.Lattice.from_file(no_use).name == "lat2"

    with_use = write(tmp_path / "with_use.pals.yaml", content + '    - use: "lat1"\n')
    assert pals.Lattice.from_file(with_use).name == "lat1"

    no_lattice = write(
        tmp_path / "no_lattice.pals.yaml",
        """\
        PALS:
          notes:
            - "no facility here"
        """,
    )
    with pytest.raises(ValueError, match="does not define a Lattice"):
        pals.Lattice.from_file(no_lattice)
