"""Tests for the commands a `facility` list can hold.

A facility entry keyed by a reserved node keyword (`set`, `sets`) is a command
rather than a lattice element. The documents used here live under
tests/pals_files/sets.
"""

import pathlib

import pydantic
import pytest

import pals

PALS_FILES = pathlib.Path(__file__).parent / "pals_files"
SETS = PALS_FILES / "sets"


def test_set_command():
    """The `set` mapping form, with and without the optional error terms."""
    root = pals.load(str(SETS / "set_command.pals.yaml"))

    assert [type(entry).__name__ for entry in root.facility] == [
        "Drift",
        "SetCommand",
        "SetCommand",
    ]

    # An expression value is recorded verbatim; this implementation builds the
    # exact representation and does not evaluate it.
    first = root.facility[1]
    assert first.parameter == "d1>length"
    assert first.value == "2 * PARAMETER"
    assert first.absolute_error is None
    assert first.relative_error is None

    # A numeric value stays numeric, and the error terms are read.
    second = root.facility[2]
    assert second.parameter == "B1.*>BendP.e1"
    assert second.value == 0.25
    assert isinstance(second.value, float)
    assert second.absolute_error == 0.001
    assert second.relative_error == 0.02


def test_set_is_not_an_element():
    """A `set` entry is a command, not an element that happens to be so named.

    Before commands were modeled, `set` satisfied the `{name: properties}`
    element shape and was read as a lattice element.
    """
    root = pals.load(str(SETS / "set_command.pals.yaml"))

    command = root.facility[1]
    assert isinstance(command, pals.SetCommand)
    assert isinstance(command, pals.FacilityCommand)
    assert not isinstance(command, pals.kinds.mixin.BaseElement)


def test_sets_compact():
    """The compact `sets` form keeps its order and its repeated parameters."""
    root = pals.load(str(SETS / "sets_compact.pals.yaml"))

    command = root.facility[1]
    assert isinstance(command, pals.SetsCommand)
    assert [(pair.parameter, pair.value) for pair in command.sets] == [
        ("d1>length", "2 * 1.5"),
        ("q1>MagneticMultipoleP.Kn1L", 0.25),
        ("d1>length", 3.0),
    ]
    # Each pair is a `set` of its own, so both forms can be read alike.
    assert all(isinstance(pair, pals.SetCommand) for pair in command.sets)


def test_set_dump():
    """Commands serialize back into the one-key form the standard writes."""
    root = pals.load(str(SETS / "set_command.pals.yaml"))
    facility = root.model_dump()["PALS"]["facility"]

    # Properties the file did not write stay out of the output.
    assert facility[1] == {"set": {"parameter": "d1>length", "value": "2 * PARAMETER"}}
    assert facility[2] == {
        "set": {
            "parameter": "B1.*>BendP.e1",
            "value": 0.25,
            "absolute_error": 0.001,
            "relative_error": 0.02,
        }
    }

    root = pals.load(str(SETS / "sets_compact.pals.yaml"))
    facility = root.model_dump()["PALS"]["facility"]
    assert facility[1] == {
        "sets": [
            {"d1>length": "2 * 1.5"},
            {"q1>MagneticMultipoleP.Kn1L": 0.25},
            {"d1>length": 3.0},
        ]
    }


@pytest.mark.parametrize("suffix", [".yaml", ".json"])
@pytest.mark.parametrize("name", ["set_command", "sets_compact"])
def test_command_roundtrip(tmp_path, name, suffix):
    """Commands survive a store/load round trip in every supported format."""
    root = pals.load(str(SETS / f"{name}.pals.yaml"))

    test_file = tmp_path / f"{name}.pals{suffix}"
    pals.store(str(test_file), root)
    reloaded = pals.load(str(test_file))

    assert reloaded == root


def test_commands_built_in_python():
    """A document assembled from command objects round trips as well."""
    root = pals.PALSroot(
        facility=[
            pals.Drift(name="d1", length=1.0),
            pals.SetCommand(parameter="d1>length", value=2.0),
            pals.SetsCommand(sets=[pals.SetCommand(parameter="d1>length", value=3.0)]),
        ]
    )

    assert isinstance(root.facility[1], pals.SetCommand)
    assert isinstance(root.facility[2], pals.SetsCommand)

    facility = root.model_dump()["PALS"]["facility"]
    assert facility[1] == {"set": {"parameter": "d1>length", "value": 2.0}}
    assert facility[2] == {"sets": [{"d1>length": 3.0}]}


def test_commands_only_in_the_facility():
    """The standard places commands in the facility, so an element list has no
    reserved keys and a `set` entry there is not read as a command."""
    line = pals.BeamLine(
        name="line",
        line=[{"set": {"parameter": "d1>length", "value": 2.0}}],
    )

    assert not isinstance(line.line[0], pals.FacilityCommand)


def test_sets_must_be_a_sequence():
    """The compact form is a sequence of pairs, not a mapping."""
    with pytest.raises(TypeError, match="'sets' command must be a list"):
        pals.load(str(SETS / "bad_sets_mapping.pals.yaml"))


def test_sets_entry_holds_one_parameter():
    """Each entry of the compact form writes exactly one parameter."""
    with pytest.raises(ValueError, match="exactly one key"):
        pals.load(str(SETS / "bad_sets_entry.pals.yaml"))


def test_set_must_be_a_mapping():
    """The `set` command holds its properties in a mapping."""
    with pytest.raises(TypeError, match="'set' command must be a dict"):
        pals.load(str(SETS / "bad_set_sequence.pals.yaml"))


def test_set_rejects_unknown_properties():
    """A misspelled property is an error, not a silently kept extra."""
    with pytest.raises(pydantic.ValidationError, match="absolut_error"):
        pals.load(str(SETS / "bad_set_key.pals.yaml"))
