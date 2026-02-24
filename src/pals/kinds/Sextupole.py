from typing import Literal

from .mixin import ThickElement
from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .utils import under_construction


@under_construction("Sextupole")
class Sextupole(ThickElement):
    """Sextupole element"""

    # Discriminator field
    kind: Literal["Sextupole"] = "Sextupole"

    # Sextupole-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
