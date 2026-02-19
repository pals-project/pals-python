"""Mixin for elements that contain lists of other elements.

This provides common YAML/JSON/... unpacking and model dumping logic for
BeamLine and UnionEle classes.
"""

from . import BaseElement
from ..PlaceholderName import PlaceholderName


def unpack_element_list_structure(
    data: dict, field_name: str, container_type: str
) -> dict:
    """Deserialize the JSON/YAML/...-like dict for element lists.

    This handles both the top-level unpacking and the field-level unpacking
    for elements that contain lists of other elements.

    Args:
        data: The input data dictionary
        field_name: Name of the field containing the element list (e.g., "line" or "elements")
        container_type: Type of container for error messages (e.g., "line" or "union")

    Returns:
        Modified data dictionary with unpacked structure
    """
    # Handle the top-level one-key dict: unpack the container's name
    if isinstance(data, dict) and len(data) == 1:
        name, value = list(data.items())[0]
        if not isinstance(value, dict):
            raise TypeError(
                f"Value for {container_type} key {name!r} must be a dict, but we got {value!r}"
            )
        value["name"] = name
        data = value

    # Handle the field: unpack each element's name
    if field_name not in data:
        raise ValueError(f"'{field_name}' field is missing")
    if not isinstance(data[field_name], list):
        raise TypeError(f"'{field_name}' must be a list")

    new_list = []
    # Loop over all elements in the list
    for item in data[field_name]:
        # An element can be a string that refers to another element
        if isinstance(item, str):
            # Wrap the string in a Placeholder name object
            new_list.append(PlaceholderName(item))
            continue
        # An element can be a PlaceholderName instance directly
        elif isinstance(item, PlaceholderName):
            # Keep the PlaceholderName as-is
            new_list.append(item)
            continue
        # An element can be a dict
        elif isinstance(item, dict):
            if not (len(item) == 1):
                raise ValueError(
                    f"Each element must be a dict with exactly one key (the element's name), "
                    f"but we got {item!r}"
                )
            name, fields = list(item.items())[0]
            if not isinstance(fields, dict):
                raise TypeError(
                    f"Value for element key {name!r} must be a dict (the element's properties), "
                    f"but we got {fields!r}"
                )
            fields["name"] = name
            new_list.append(fields)
        # An element can be an instance of an existing model
        else:
            # Try to check if it's a BaseElement instance
            if isinstance(item, BaseElement):
                # Nothing to do, keep the element as is
                new_list.append(item)
                continue

            raise TypeError(
                f"Value must be a reference string, PlaceholderName, or a dict, but we got {item!r}"
            )

    data[field_name] = new_list
    return data


def dump_element_list(self, field_name: str, *args, **kwargs) -> dict:
    """Serialize to JSON/YAML/... via a custom pydantic model dump for element lists.

    This makes sure the element name property is moved out and up to a one-key dictionary.

    Args:
        self: The model instance
        field_name: Name of the field containing the element list (e.g., "line" or "elements")
        *args: Positional arguments for model_dump
        **kwargs: Keyword arguments for model_dump

    Returns:
        Serialized data dictionary
    """
    # Use base element dump first and return a dict {key: value}, where 'key'
    # is the name of the container and 'value' is a dict with all other properties
    data = super(type(self), self).model_dump(*args, **kwargs)

    # Reformat field as a list of element dicts
    new_list = []
    element_list = getattr(self, field_name)
    for elem in element_list:
        # Use a custom dump for each element, which now returns a dict
        elem_dict = elem.model_dump(**kwargs)
        new_list.append(elem_dict)

    if hasattr(self, "name"):  # all but PALSroot have a name
        data[self.name][field_name] = new_list
    else:
        data[field_name] = new_list
    return data
