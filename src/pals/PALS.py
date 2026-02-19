from pydantic import BaseModel

from pydantic import model_validator
from typing import List, Optional

from .kinds import Lattice
from .kinds.all_elements import get_all_elements_as_annotation
from .functions import load_file_to_dict, store_dict_to_file


Facility = List[get_all_elements_as_annotation()]


class PALSroot(BaseModel):
    """Represent the roo PALS structure"""

    version: Optional[str] = None

    facility: Facility

    @model_validator(mode="before")
    @classmethod
    def unpack_json_structure(cls, data):
        """Deserialize the JSON/YAML/...-like dict for facility elements"""
        from pals.kinds.mixin.all_element_mixin import unpack_element_list_structure

        return unpack_element_list_structure(data, "facility", "facility")

    def model_dump(self, *args, **kwargs):
        """Custom model dump for facility to handle element list formatting"""
        from pals.kinds.mixin.all_element_mixin import dump_element_list

        data = {}
        data["PALS"] = {}
        data["PALS"]["version"] = self.version
        data["PALS"] = dump_element_list(self, "facility", *args, **kwargs)
        return data

    @staticmethod
    def from_file(filename: str) -> "PALSroot":
        """Load a facility from a text file"""
        pals_dict = load_file_to_dict(filename)
        return PALSroot(**pals_dict)

    def to_file(self, filename: str):
        """Save a facility to a text file"""
        pals_dict = self.model_dump()
        store_dict_to_file(filename, pals_dict)


def load(filename: str) -> PALSroot:
    """Load a facility from a text file"""
    pals_dict = load_file_to_dict(filename)
    return PALSroot(**pals_dict)


def store(filename: str, pals_root: PALSroot | Facility | Lattice):
    # wrap single elements in a list, facility in a PALSroot
    if isinstance(pals_root, Lattice):
        pals_root = PALSroot(version=None, facility=[pals_root])
    elif isinstance(pals_root, list):
        pals_root = PALSroot(version=None, facility=pals_root)

    pals_dict = pals_root.model_dump()
    store_dict_to_file(filename, pals_dict)
