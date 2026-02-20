from pydantic import model_validator  # noqa
from typing import Literal

from .all_elements import get_all_elements_as_annotation
from .mixin import BaseElement


class UnionEle(BaseElement):
    """Union element for overlapping elements"""

    # Discriminator field
    kind: Literal["UnionEle"] = "UnionEle"

    # Elements in the union - uses the same union type as BeamLine
    elements: list[get_all_elements_as_annotation()] = []

    @model_validator(mode="before")
    @classmethod
    def unpack_json_structure(cls, data):
        """Deserialize the JSON/YAML/...-like dict for UnionEle elements"""
        from pals.kinds.mixin.all_element_mixin import unpack_element_list_structure

        return unpack_element_list_structure(data, "elements", "union")

    def model_dump(self, *args, **kwargs):
        """Custom model dump for UnionEle to handle element list formatting"""
        from pals.kinds.mixin.all_element_mixin import dump_element_list

        return dump_element_list(self, "elements", *args, **kwargs)
