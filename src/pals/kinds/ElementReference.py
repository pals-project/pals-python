"""Element reference class for referring to elements by name."""

from pydantic import BaseModel, Field, model_serializer
from typing import Annotated

from .mixin import BaseElement


class ElementReference(BaseModel):
    """A pydantic model that represents a reference to a named element.

    This class behaves like a string (via __str__ and __eq__) but stores
    a true reference to the actual element object once it's resolved.

    The element field holds a reference (not a copy) to the actual element.

    Attributes:
        name: The name of the referenced element
        element: A reference to the resolved element object (None until resolved)

    Example:
        >>> ref = ElementReference(name="drift1")
        >>> ref.name
        'drift1'
        >>> str(ref)
        'drift1'
        >>> ref == "drift1"
        True
        >>> ref.element  # None until resolved
        >>> drift = pals.Drift(name="drift1", length=1.0)
        >>> ref.element = drift
        >>> ref.is_resolved()
        True
        >>> ref.element is drift  # True - it's a reference, not a copy
        True
    """

    name: str = Field(..., description="The name of the referenced element")
    element: Annotated[
        "BaseElement | None",
        Field(default=None, description="Reference to the resolved element object"),
    ] = None

    @model_serializer(mode="plain")
    def _serialize_as_name(self) -> str:
        """Serialize this reference as just its name.

        This makes `model_dump()` return a string (the element name), so nested
        serialization (e.g. inside BeamLine.line) produces plain strings too.
        """
        return self.name

    def __init__(self, name: str | None = None, /, **data):
        """Initialize with either positional name or keyword arguments."""
        if name is not None:
            super().__init__(name=name, **data)
        else:
            super().__init__(**data)

    def __str__(self) -> str:
        """Return the element name as string."""
        return self.name

    def __eq__(self, other: object) -> bool:
        """Enable string comparison."""
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, ElementReference):
            return self.name == other.name and self.element is other.element
        return False

    def __hash__(self) -> int:
        """Make hashable like a string."""
        return hash(self.name)

    def is_resolved(self) -> bool:
        """Check if this reference has been resolved to an actual element."""
        return self.element is not None

    def __repr__(self) -> str:
        """Return a representation of the ElementReference."""
        resolved = "resolved" if self.is_resolved() else "unresolved"
        return f"ElementReference('{self.name}', {resolved})"
