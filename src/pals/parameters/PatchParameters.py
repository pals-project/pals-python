from typing import Literal

from pydantic import BaseModel


class PatchParameters(BaseModel):
    """Patch parameters"""

    x_offset: float = 0.0
    y_offset: float = 0.0
    z_offset: float = 0.0
    x_rot: float = 0.0
    y_rot: float = 0.0
    z_rot: float = 0.0
    flexible: bool = False
    ref_coords: Literal["entrance_end", "exit_end"] = "exit_end"
    user_sets_length: bool = False
