from pydantic import BaseModel


# A command value is either a number or an expression written as a string, per
# the standard's Expression type. Expressions are recorded verbatim: this
# implementation builds the exact representation of a PALS file and does not
# evaluate them.
CommandValue = bool | int | float | str | None


class FacilityCommand(BaseModel, extra="forbid"):
    """A `facility` entry that is a command rather than a lattice element.

    Element entries are one-key mappings whose key is the element's name;
    command entries are one-key mappings whose key is a reserved node keyword
    (`set`, `sets`, ...). Commands keep their place in the ordered `facility`
    list, because the standard's lattice expansion only lets a command act on
    what was defined before it.
    """
