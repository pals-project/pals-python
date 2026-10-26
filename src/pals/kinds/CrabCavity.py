from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("CrabCavity")
class CrabCavity(ThickElement):
    """RF crab cavity"""

    # Discriminator field
    kind: Literal["CrabCavity"] = "CrabCavity"

    # CrabCavity-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
