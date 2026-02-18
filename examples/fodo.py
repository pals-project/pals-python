from pals import MagneticMultipoleParameters
from pals import Drift
from pals import Quadrupole
from pals import BeamLine
from pals import Lattice


def main():
    drift1 = Drift(
        name="drift1",
        length=0.25,
    )
    quad1 = Quadrupole(
        name="quad1",
        length=1.0,
        MagneticMultipoleP=MagneticMultipoleParameters(
            Bn1=1.0,
        ),
    )
    drift2 = Drift(
        name="drift2",
        length=0.5,
    )
    quad2 = Quadrupole(
        name="quad2",
        length=1.0,
        MagneticMultipoleP=MagneticMultipoleParameters(
            Bn1=-1.0,
        ),
    )
    drift3 = Drift(
        name="drift3",
        length=0.5,
    )
    # Create line with all elements
    line = BeamLine(
        name="fodo_cell",
        line=[
            drift1,
            quad1,
            drift2,
            quad2,
            drift3,
        ],
    )
    # Create lattice with the line as a branch
    lattice = Lattice(
        name="fodo_lattice",
        branches=[line],
    )

    # Serialize to YAML
    yaml_file = "examples_fodo.pals.yaml"
    lattice.to_file(yaml_file)

    # Read YAML data from file
    loaded_lattice = Lattice.from_file(yaml_file)

    # Validate loaded data
    assert lattice == loaded_lattice

    # Serialize to JSON
    json_file = "examples_fodo.pals.json"
    lattice.to_file(json_file)

    # Read JSON data from file
    loaded_lattice = Lattice.from_file(json_file)

    # Validate loaded data
    assert lattice == loaded_lattice


if __name__ == "__main__":
    main()
