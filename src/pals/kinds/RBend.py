from typing import Literal

from ..parameters import (
    BendParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)
from .mixin import ThickElement


class RBend(ThickElement):
    """A rectangular bend element"""

    # Discriminator field
    kind: Literal["RBend"] = "RBend"

    # Bend-specific parameters
    BendP: BendParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
