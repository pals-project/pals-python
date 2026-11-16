from typing import Literal

from ..parameters import FloorShiftParameters
from .mixin import BaseElement


class FloorShift(BaseElement):
    """Global coordinates shift element"""

    # Discriminator field
    kind: Literal["FloorShift"] = "FloorShift"

    # Floor shift-specific parameters
    FloorShiftP: FloorShiftParameters | None = None
