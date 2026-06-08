from typing import Literal

from .mixin import ThickElement
from ..parameters import (
    BendParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)


class RBend(ThickElement):
    """A rectangular bend element"""

    # Discriminator field
    kind: Literal["RBend"] = "RBend"

    # Bend-specific parameters
    BendP: BendParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
