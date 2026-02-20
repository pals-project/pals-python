from typing import Literal

from .mixin import ThickElement
from ..parameters import (
    SolenoidParameters,
    ElectricMultipoleParameters,
    MagneticMultipoleParameters,
)
from .utils import under_construction


@under_construction("Solenoid")
class Solenoid(ThickElement):
    """Solenoid element"""

    # Discriminator field
    kind: Literal["Solenoid"] = "Solenoid"

    # Solenoid-specific parameters
    SolenoidP: SolenoidParameters | None = None

    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
