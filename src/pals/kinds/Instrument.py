from typing import Literal

from .mixin import ThickElement
from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .utils import under_construction


@under_construction("Instrument")
class Instrument(ThickElement):
    """Measurement element"""

    # Discriminator field
    kind: Literal["Instrument"] = "Instrument"

    # Instrument-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
