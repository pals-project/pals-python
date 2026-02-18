"""Helper module to define the union of all allowed element types.

This module creates a helper function that returns the element union type,
avoiding duplication between BeamLine.line and UnionEle.elements.
"""

from typing import Annotated, Union

from pydantic import Field

from .ACKicker import ACKicker
from .BeamBeam import BeamBeam
from .BeginningEle import BeginningEle
from .Converter import Converter
from .CrabCavity import CrabCavity
from .Drift import Drift
from .EGun import EGun
from .Feedback import Feedback
from .Fiducial import Fiducial
from .FloorShift import FloorShift
from .Foil import Foil
from .Fork import Fork
from .Girder import Girder
from .Instrument import Instrument
from .Kicker import Kicker
from .Marker import Marker
from .Mask import Mask
from .Match import Match
from .Multipole import Multipole
from .NullEle import NullEle
from .Octupole import Octupole
from .Patch import Patch
from .Quadrupole import Quadrupole
from .RBend import RBend
from .RFCavity import RFCavity
from .SBend import SBend
from .Sextupole import Sextupole
from .Solenoid import Solenoid
from .Taylor import Taylor
from .Wiggler import Wiggler


def get_all_element_types(extra_types: tuple = None):
    """Return a tuple of all element types that can be used in BeamLine or UnionEle."""
    element_types = (
        "Lattice",  # Forward reference to handle circular import
        "BeamLine",  # Forward reference to handle circular import
        "UnionEle",  # Forward reference to handle circular import
        ACKicker,
        BeamBeam,
        BeginningEle,
        Converter,
        CrabCavity,
        Drift,
        EGun,
        Feedback,
        Fiducial,
        FloorShift,
        Foil,
        Fork,
        Girder,
        Instrument,
        Kicker,
        Marker,
        Mask,
        Match,
        Multipole,
        NullEle,
        Octupole,
        Patch,
        Quadrupole,
        RBend,
        RFCavity,
        SBend,
        Sextupole,
        Solenoid,
        Taylor,
        Wiggler,
    )
    if extra_types is not None:
        element_types += extra_types
    return element_types


def get_all_elements_as_annotation(extra_types: tuple = None):
    """Return the Union type of all allowed elements with their name as the discriminator field.

    Note: When str is included in the union (for string references), we cannot use
    discriminator since str doesn't have a 'kind' field. Pydantic will still properly
    validate the union by trying each type in order.
    """
    types = get_all_element_types(extra_types)
    # Add str to support string references to named elements
    # We can't use discriminator with str in the union since str has no 'kind' field
    return Union[types + (str,)]
