from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("Kicker")
class Kicker(ThickElement):
    """Particle kicker element"""

    # Discriminator field
    kind: Literal["Kicker"] = "Kicker"

    # Kicker-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
