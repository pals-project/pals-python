from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("Multipole")
class Multipole(ThickElement):
    """Multipole element"""

    # Discriminator field
    kind: Literal["Multipole"] = "Multipole"

    # Multipole-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
