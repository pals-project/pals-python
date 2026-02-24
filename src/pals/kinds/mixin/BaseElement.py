from pydantic import BaseModel
from typing import Literal

from pals.parameters import (
    ApertureParameters,
    BodyShiftParameters,
    FloorParameters,
    MetaParameters,
    ReferenceParameters,
    ReferenceChangeParameters,
    TrackingParameters,
)


class BaseElement(BaseModel, validate_assignment=True):
    """A custom base element defining common properties"""

    # Discriminator field
    kind: Literal["BaseElement"] = "BaseElement"

    # element name
    name: str

    # Common parameter groups (optional for all elements)
    ApertureP: ApertureParameters | None = None
    BodyShiftP: BodyShiftParameters | None = None
    FloorP: FloorParameters | None = None
    MetaP: MetaParameters | None = None
    ReferenceP: ReferenceParameters | None = None
    ReferenceChangeP: ReferenceChangeParameters | None = None
    TrackingP: TrackingParameters | None = None

    def model_dump(self, *args, **kwargs):
        """This makes sure the element name property is moved out and up to a one-key dictionary"""
        # Exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        elem_dict = super().model_dump(*args, **kwargs)
        name = elem_dict.pop("name", None)
        if name is None:
            raise ValueError("Element missing 'name' attribute")
        # Return a dict {name: properties} rather than a single-item list
        # This makes the serialized form a plain dict so it can be passed to
        # constructors using keyword expansion (e.g., Model(**data))
        data = {name: elem_dict}
        return data
