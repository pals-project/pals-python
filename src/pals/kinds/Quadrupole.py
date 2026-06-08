from typing import Literal, Self

from pydantic import model_validator

from .mixin import ThickElement
from ..parameters import MagneticMultipoleParameters, ElectricMultipoleParameters


class Quadrupole(ThickElement):
    """Quadrupole element"""

    # Discriminator field
    kind: Literal["Quadrupole"] = "Quadrupole"

    # Quadrupole-specific parameters
    MagneticMultipoleP: MagneticMultipoleParameters | None = None
    ElectricMultipoleP: ElectricMultipoleParameters | None = None

    @model_validator(mode="after")
    def validate_at_least_one_multipole(self) -> Self:
        """Ensure at least one multipole parameter is specified."""
        if self.MagneticMultipoleP is None and self.ElectricMultipoleP is None:
            raise ValueError(
                "At least one of 'MagneticMultipoleP' or 'ElectricMultipoleP' must be specified"
            )
        return self
