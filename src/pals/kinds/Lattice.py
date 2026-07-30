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
        """Load a Lattice from a text file.

        The file can hold either a single Lattice or a full PALS document.
        Per the standard's use statement, the lattice instantiated from a full
        document is the last one defined, unless a `use` entry selects another.
        """
        pals_dict = load_file_to_dict(filename)

        if isinstance(pals_dict, dict) and "PALS" in pals_dict:
            from pals.PALS import PALSroot
            from pals.kinds.PlaceholderName import PlaceholderName

            pals_root = PALSroot(**pals_dict)
            facility = pals_root.facility or []
            lattices = [item for item in facility if isinstance(item, Lattice)]
            by_name = {lattice.name: lattice for lattice in lattices}

            # A `use` entry overrides the last-lattice default; with several,
            # the last one wins. It must name a Lattice the document defines.
            use_entries = [
                item
                for item in facility
                if isinstance(item, PlaceholderName) and item.is_use
            ]
            if use_entries:
                selected = use_entries[-1].name
                if selected not in by_name:
                    raise ValueError(
                        f"PALS root document {filename!r} selects {selected!r} "
                        f"with its use entry, but defines no Lattice of that "
                        f"name; defined Lattices: {sorted(by_name)}"
                    )
                return by_name[selected]

            if not lattices:
                raise ValueError(
                    f"PALS root document {filename!r} does not define a Lattice"
                )
            return lattices[-1]

        return Lattice(**pals_dict)

    def to_file(self, filename: str):
        """Save a Lattice to a text file"""
        pals_dict = self.model_dump()
        store_dict_to_file(filename, pals_dict)
