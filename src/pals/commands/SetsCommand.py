from pydantic import model_serializer

from .FacilityCommand import FacilityCommand
from .SetCommand import SetCommand


class SetsCommand(FacilityCommand):
    """The compact `sets` command: a sequence of parameter/value pairs.

    See the standard's Setting Parameters section, which offers this form for
    sets that only have a value:

    ```yaml
    - sets:
        - param1: value1
        - param2: value2
    ```

    Each pair is held as a `SetCommand`, so a reader can treat the compact form
    and the `set` form alike; the compact form is what gets written back out.
    Being a sequence, it keeps its order and may name the same parameter twice.

    Note that `sets` is a reserved key of the `facility` list: an element cannot
    be named `sets`.
    """

    sets: list[SetCommand]

    @model_serializer(mode="plain")
    def _serialize_as_command(self) -> dict:
        """Serialize back into the one-key `sets:` form the standard writes."""
        return {"sets": [{pair.parameter: pair.value} for pair in self.sets]}
