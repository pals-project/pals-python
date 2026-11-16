from typing import Annotated, Literal

from annotated_types import Ge
from pydantic import BaseModel


class RFParameters(BaseModel):
    """RF parameters"""

    frequency: Annotated[float, Ge(0.0)] = 0.0  # [Hz] RF frequency
    harmon: Annotated[int, Ge(0)] = 0  # [unitless] RF frequency harmonic number
    voltage: float = 0.0  # [V] RF voltage
    gradient: float = 0.0  # [V/m] RF gradient
    phase: float = 0.0  # [unitless] RF phase in 0 to 2*pi
    multipass_phase: float = 0.0  # [unitless] RF Phase added to multipass elements
    cavity_type: Literal["STANDING_WAVE"] = "STANDING_WAVE"  # [string] Cavity type
    n_cell: Annotated[int, Ge(1)] = 1  # [unitless] Number of cavity cells
