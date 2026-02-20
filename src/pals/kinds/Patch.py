from typing import Literal

from .mixin import ThickElement
from ..parameters import PatchParameters
from .utils import under_construction


@under_construction("Patch")
class Patch(ThickElement):
    """Crooked drift used to shift the reference curve"""

    # Discriminator field
    kind: Literal["Patch"] = "Patch"

    # Patch-specific parameters
    PatchP: PatchParameters | None = None
