from typing import Literal

from ..parameters import (
    BendParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)
from .mixin import ThickElement


class SBend(ThickElement):
    """A sector bend element"""

    # Discriminator field
    kind: Literal["SBend"] = "SBend"

    # Bend-specific parameters
    BendP: BendParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
