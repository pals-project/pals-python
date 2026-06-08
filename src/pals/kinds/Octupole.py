from typing import Literal

from .mixin import ThickElement
from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .utils import under_construction


@under_construction("Octupole")
class Octupole(ThickElement):
    """Octupole element"""

    # Discriminator field
    kind: Literal["Octupole"] = "Octupole"

    # Octupole-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
