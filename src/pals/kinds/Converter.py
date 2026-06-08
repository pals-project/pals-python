from typing import Literal

from .mixin import BaseElement
from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .utils import under_construction


@under_construction("Converter")
class Converter(BaseElement):
    """Target to produce new species. EG: Positron converter"""

    # Discriminator field
    kind: Literal["Converter"] = "Converter"

    # Converter-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
