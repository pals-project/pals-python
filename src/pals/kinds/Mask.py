from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("Mask")
class Mask(ThickElement):
    """Collimation element"""

    # Discriminator field
    kind: Literal["Mask"] = "Mask"

    # Mask-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
