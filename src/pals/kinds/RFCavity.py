from typing import Literal

from ..parameters import (
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
    RFParameters,
    SolenoidParameters,
)
from .mixin import ThickElement
from .utils import under_construction


@under_construction("RFCavity")
class RFCavity(ThickElement):
    """RF cavity element"""

    # Discriminator field
    kind: Literal["RFCavity"] = "RFCavity"

    # RF-specific parameters
    RFP: RFParameters | None = None
    SolenoidP: SolenoidParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
