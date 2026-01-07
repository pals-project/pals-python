from pals import MagneticMultipoleParameters
from pals import Drift
from pals import Quadrupole
from pals import BeamLine


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

    # Serialize to YAML
    yaml_file = "examples_fodo.pals.yaml"
    line.to_file(yaml_file)

    # Read YAML data from file
    loaded_line = BeamLine.from_file(yaml_file)

    # Validate loaded data
    assert line == loaded_line

    # Serialize to JSON
    json_file = "examples_fodo.pals.json"
    line.to_file(json_file)

    # Read JSON data from file
    loaded_line = BeamLine.from_file(json_file)

    # Validate loaded data
    assert line == loaded_line


if __name__ == "__main__":
    main()
