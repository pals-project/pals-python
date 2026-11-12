from typing import Literal

from pydantic import BaseModel


class ReferenceParameters(BaseModel):
    """Reference parameters"""

    species_ref: str = ""
    pc_ref: float = 0.0  # [momentum*c] Reference momentum times speed of light
    E_tot_ref: float = 0.0  # [eV] Reference total energy
    time_ref: float = 0.0  # [s] Reference time
    # TODO: not defined in PALS
    location: Literal["UPSTREAM_END", "DOWNSTREAM_END"] | None = None
