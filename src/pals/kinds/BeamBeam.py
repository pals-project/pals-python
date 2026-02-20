from typing import Literal

from .mixin import BaseElement
from ..parameters import BeamBeamParameters
from .utils import under_construction


@under_construction("BeamBeam")
class BeamBeam(BaseElement):
    """Element for simulating colliding beams"""

    # Discriminator field
    kind: Literal["BeamBeam"] = "BeamBeam"

    # Beam-beam-specific parameters
    BeamBeamP: BeamBeamParameters | None = None
