from typing import Literal

from ..parameters import BeamBeamParameters
from .mixin import BaseElement
from .utils import under_construction


@under_construction("BeamBeam")
class BeamBeam(BaseElement):
    """Element for simulating colliding beams"""

    # Discriminator field
    kind: Literal["BeamBeam"] = "BeamBeam"

    # Beam-beam-specific parameters
    BeamBeamP: BeamBeamParameters | None = None
