from pydantic import model_validator
from typing import Literal, Self

from .BeamLine import BeamLine
from .PlaceholderName import PlaceholderName
from .mixin import BaseElement
from ..functions import load_file_to_dict, store_dict_to_file


class Lattice(BaseElement):
    """A lattice combines beamlines"""

    kind: Literal["Lattice"] = "Lattice"

    branches: list[BeamLine | PlaceholderName]

    @model_validator(mode="before")
    @classmethod
    def unpack_json_structure(cls, data):
        """Deserialize the JSON/YAML/...-like dict for Lattice elements"""
        from pals.kinds.mixin.all_element_mixin import unpack_element_list_structure

        return unpack_element_list_structure(data, "branches", "branches")

    def model_dump(self, *args, **kwargs):
        """Custom model dump for Lattice to handle element list formatting"""
        from pals.kinds.mixin.all_element_mixin import dump_element_list

        return dump_element_list(self, "branches", *args, **kwargs)

    @staticmethod
    def from_file(filename: str) -> Self:
        """Load a Lattice from a text file"""
        pals_dict = load_file_to_dict(filename)

        if isinstance(pals_dict, dict) and "PALS" in pals_dict:
            # Full PALS documents select their active lattice with a facility-level use.
            from pals.PALS import PALSroot
            from pals.kinds.PlaceholderName import PlaceholderName

            pals_root = PALSroot(**pals_dict)
            use_name = None
            for item in pals_root.facility:
                if isinstance(item, PlaceholderName):
                    use_name = item.name

            if use_name is None:
                raise ValueError("PALS root document does not specify a lattice to use")

            # Return the selected lattice while preserving the existing direct-lattice path.
            for item in pals_root.facility:
                if isinstance(item, Lattice) and item.name == use_name:
                    return item

            raise ValueError(f"PALS root document does not define lattice {use_name!r}")

        return Lattice(**pals_dict)

    def to_file(self, filename: str):
        """Save a Lattice to a text file"""
        pals_dict = self.model_dump()
        store_dict_to_file(filename, pals_dict)
