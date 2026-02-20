from typing import Literal

from .mixin import BaseElement
from ..parameters import FloorShiftParameters


class FloorShift(BaseElement):
    """Global coordinates shift element"""

    # Discriminator field
    kind: Literal["FloorShift"] = "FloorShift"

    # Floor shift-specific parameters
    FloorShiftP: FloorShiftParameters | None = None
