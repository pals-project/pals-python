from typing import Literal

from .mixin import ThickElement
from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .utils import under_construction


@under_construction("CrabCavity")
class CrabCavity(ThickElement):
    """RF crab cavity"""

    # Discriminator field
    kind: Literal["CrabCavity"] = "CrabCavity"

    # CrabCavity-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
