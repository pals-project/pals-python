import pals


def test_include(tmp_path):
    main_file = tmp_path / "main.pals.yaml"
    root_included_file = tmp_path / "included.pals.yaml"
    facility_included_file = tmp_path / "facility.pals.yaml"
    facility_nested_file = tmp_path / "facility_nested.pals.yaml"

    main_content = f"""
    PALS:
      include: "{root_included_file.name}"
      facility:
        - drift1:
            kind: Drift
            length: 0.25

        - include: "{facility_included_file.name}"

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
    """

    root_included_content = """
    author: "Some One <name@email.com>"
    version: 1.0
    """

    facility_included_content = f"""
    - quad1:
        kind: Quadrupole
        MagneticMultipoleP:
          Bn1: 1.0
        length: 1.0

    - drift2:
        kind: Drift
        length: 0.5
    
    - include: "{facility_nested_file.name}"
    """

    facility_nested_content = """
        - quad2:
            kind: Quadrupole
            MagneticMultipoleP:
              Bn1: -1.0
            length: 1.0
        """

    main_file.write_text(main_content)
    root_included_file.write_text(root_included_content)
    facility_included_file.write_text(facility_included_content)
    facility_nested_file.write_text(facility_nested_content)

    data = pals.Lattice.from_file(main_file)

    assert data["PALS"]["version"] == 1.0
    assert data["PALS"]["other"] == "value"
    assert data["PALS"]["author"] == "Some One <name@email.com>"
    assert "include" not in data["PALS"]


def test_nested_include(tmp_path):
    root_file = tmp_path / "root.pals.yaml"
    middle_file = tmp_path / "middle.pals.yaml"
    leaf_file = tmp_path / "leaf.pals.yaml"

    root_content = f"""
    root:
      include: "{middle_file.name}"
    """

    middle_content = f"""
    middle: val
    include: "{leaf_file.name}"
    """

    leaf_content = """
    leaf: val
    """

    root_file.write_text(root_content)
    middle_file.write_text(middle_content)
    leaf_file.write_text(leaf_content)

    data = pals.functions.load_file_to_dict(str(root_file))

    assert data["root"]["middle"] == "val"
    assert data["root"]["leaf"] == "val"
    assert "include" not in data["root"]


def test_include_list_into_dict_conversion(tmp_path):
    # This tests the spec example where a list of properties is included into a dict (element)
    main_file = tmp_path / "element.pals.yaml"
    params_file = tmp_path / "params.pals.yaml"

    main_content = f"""
    element:
      kind: Quadrupole
      include: "{params_file.name}"
    """

    # params file content is a list of single-key dicts
    params_content = """
    - MagneticMultipoleP:
      - Kn3L: 0.3
    - ApertureP:
        x_limits: [-0.1, 0.1]
    """

    main_file.write_text(main_content)
    params_file.write_text(params_content)

    data = pals.functions.load_file_to_dict(str(main_file))

    elem = data["element"]
    assert elem["kind"] == "Quadrupole"

    # Check if keys are correctly merged from the list
    assert "MagneticMultipoleP" in elem
    assert elem["MagneticMultipoleP"] == [{"Kn3L": 0.3}]

    assert "ApertureP" in elem
    assert elem["ApertureP"] == {"x_limits": [-0.1, 0.1]}
