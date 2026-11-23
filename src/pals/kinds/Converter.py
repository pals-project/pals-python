from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import BaseElement
from .utils import under_construction


@under_construction("Converter")
class Converter(BaseElement):
    """Target to produce new species. EG: Positron converter"""

    # Discriminator field
    kind: Literal["Converter"] = "Converter"

    # Converter-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
