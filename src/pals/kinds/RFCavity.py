from typing import Literal

from .mixin import ThickElement
from ..parameters import (
    RFParameters,
    SolenoidParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)
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
