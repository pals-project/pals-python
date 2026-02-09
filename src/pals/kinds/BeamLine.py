from pydantic import model_validator
from typing import List, Literal

from .all_elements import get_all_elements_as_annotation
from .mixin import BaseElement
from ..functions import load_file_to_dict, store_dict_to_file


class BeamLine(BaseElement):
    """A line of elements and/or other lines"""

    kind: Literal["BeamLine"] = "BeamLine"

    line: List[get_all_elements_as_annotation()]

    @model_validator(mode="before")
    @classmethod
    def unpack_json_structure(cls, data):
        """Deserialize the JSON/YAML/...-like dict for BeamLine elements"""
        from pals.kinds.mixin.all_element_mixin import unpack_element_list_structure

        return unpack_element_list_structure(data, "line", "line")

    def model_dump(self, *args, **kwargs):
        """Custom model dump for BeamLine to handle element list formatting"""
        from pals.kinds.mixin.all_element_mixin import dump_element_list

        return dump_element_list(self, "line", *args, **kwargs)

    @staticmethod
    def from_file(filename: str) -> "BeamLine":
        """Load a BeamLine from a text file"""
        pals_dict = load_file_to_dict(filename)
        return BeamLine(**pals_dict)

    def to_file(self, filename: str):
        """Save a BeamLine to a text file"""
        pals_dict = self.model_dump()
        store_dict_to_file(filename, pals_dict)
