from typing import Literal

from .mixin import BaseElement


class Marker(BaseElement):
    """Zero length element to mark a particular position

    The main purpose of this thin element is to name a position in the beamline.
    """

    # Discriminator field
    kind: Literal["Marker"] = "Marker"

    # Segment length in meters (m)
    # Always 0, cannot be modified
    length: Literal[0.0] = 0.0
