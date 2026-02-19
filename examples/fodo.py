from pals import MagneticMultipoleParameters
from pals import Drift
from pals import Quadrupole
from pals import BeamLine
from pals import Lattice
from pals import load, store


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
    store(yaml_file, lattice)

    # Read YAML data from file
    loaded_lattice = load(yaml_file)

    # Validate loaded data
    assert lattice == loaded_lattice.facility[0]

    # Serialize to JSON
    json_file = "examples_fodo.pals.json"
    store(json_file, lattice)

    # Read JSON data from file
    loaded_lattice = load(json_file)

    # Validate loaded data
    assert lattice == loaded_lattice.facility[0]


if __name__ == "__main__":
    main()
