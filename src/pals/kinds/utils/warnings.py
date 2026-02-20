"""
Utility module for handling warnings for under construction elements.
"""

import warnings
from typing import TypeVar

T = TypeVar("T", bound=type)


def under_construction(element_name: str | None = None):
    """
    Compact decorator to mark an element as under construction.

    Usage:
        @under_construction("ElementName")
        class MyElement(BaseElement):
            pass

    Args:
        element_name: Optional custom name for the element. If not provided,
                     uses the class name.
    """

    def decorator(cls: T) -> T:
        # Store original __init__ method
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            # Call original __init__ first
            original_init(self, *args, **kwargs)
            # Issue warning after initialization
            name = element_name or cls.__name__
            warnings.warn(
                f"The {name} element is marked as 'Under Construction' in the PALS standard. "
                f"Please refer to the PALS documentation for current status and limitations.",
                UserWarning,
                stacklevel=3,
            )

        # Replace __init__ method
        cls.__init__ = new_init

        # Add warning to class docstring if not already present
        if (
            not hasattr(cls, "__doc__")
            or not cls.__doc__
            or "UNDER CONSTRUCTION" not in cls.__doc__.upper()
        ):
            original_doc = cls.__doc__ or ""
            warning_doc = f"""
**UNDER CONSTRUCTION**: This element is marked as 'Under Construction' in the PALS standard.

{original_doc.strip()}

**Warning**: This element implementation may be incomplete or subject to change.
Please refer to the PALS documentation for the current status and any limitations.
"""
            cls.__doc__ = warning_doc.strip()

        return cls

    return decorator
