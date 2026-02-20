from typing import Literal

from .mixin import ThickElement
from ..parameters import (
    BendParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)


class SBend(ThickElement):
    """A sector bend element"""

    # Discriminator field
    kind: Literal["SBend"] = "SBend"

    # Bend-specific parameters
    BendP: BendParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
