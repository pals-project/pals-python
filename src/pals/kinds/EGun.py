from typing import Literal

from ..parameters import ElectricMultipoleParameters, MagneticMultipoleParameters
from .mixin import ThickElement
from .utils import under_construction


@under_construction("EGun")
class EGun(ThickElement):
    """Electron gun"""

    # Discriminator field
    kind: Literal["EGun"] = "EGun"

    # EGun-specific parameters
    ElectricMultipoleP: ElectricMultipoleParameters | None = None
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
