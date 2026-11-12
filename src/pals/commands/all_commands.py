"""Helper module that knows every command the `facility` list can hold.

This is the one place that maps a reserved node keyword (`set`, `sets`, ...) to
the model that holds it, so adding a command means touching this module and
nothing else.
"""

from .FacilityCommand import FacilityCommand
from .SetCommand import SetCommand
from .SetsCommand import SetsCommand


def _build_set(body) -> SetCommand:
    """Build a `set` command from its properties mapping."""
    if not isinstance(body, dict):
        raise TypeError(
            f"Value for the 'set' command must be a dict (the command's properties), "
            f"but we got {body!r}"
        )
    return SetCommand(**body)


def _build_sets(body) -> SetsCommand:
    """Build a `sets` command from its sequence of parameter/value pairs."""
    if not isinstance(body, list):
        raise TypeError(
            f"Value for the 'sets' command must be a list of parameter/value pairs, "
            f"but we got {body!r}"
        )

    pairs = []
    for entry in body:
        if not isinstance(entry, dict) or len(entry) != 1:
            raise ValueError(
                f"Each 'sets' entry must be a dict with exactly one key (the "
                f"parameter to set), but we got {entry!r}"
            )
        parameter, value = next(iter(entry.items()))
        pairs.append(SetCommand(parameter=parameter, value=value))

    return SetsCommand(sets=pairs)


# Reserved keys of the `facility` list, and how to build what they hold. A
# facility entry keyed by one of these is a command, not an element, so an
# element cannot carry one of these names.
_COMMAND_BUILDERS = {
    "set": _build_set,
    "sets": _build_sets,
}


def get_all_command_types() -> tuple:
    """Return a tuple of all command types that can appear in a facility."""
    return (SetCommand, SetsCommand)


def build_facility_command(item) -> FacilityCommand | None:
    """Build the command a raw facility entry holds.

    Args:
        item: One raw entry of the `facility` list

    Returns:
        The command, or None if the entry is not a command and should be
        unpacked as a lattice element instead
    """
    if not isinstance(item, dict) or len(item) != 1:
        return None

    keyword, body = next(iter(item.items()))
    builder = _COMMAND_BUILDERS.get(keyword)
    if builder is None:
        return None

    return builder(body)
