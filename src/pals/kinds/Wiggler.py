from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("Wiggler")
class Wiggler(ThickElement):
    """Wiggler element"""

    # Discriminator field
    kind: Literal["Wiggler"] = "Wiggler"

    # Wiggler-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
