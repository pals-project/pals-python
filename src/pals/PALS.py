from pydantic import BaseModel

from pydantic import model_validator
from typing import Self

from .kinds import Lattice
from .kinds.all_elements import get_all_elements_as_annotation
from .functions import load_file_to_dict, store_dict_to_file


Facility = list[get_all_elements_as_annotation()]


class Author(BaseModel):
    """An author associated with a PALS file.

    Authors are optional, but recommended to enable data provenance and
    contacts. Only the name is required.
    """

    name: str
    orcid: str | None = None
    affiliation: str | None = None
    email: str | None = None


class ExtensionLabels(BaseModel, extra="forbid"):
    """Registered extension labels, see the standard's Extensions chapter.

    Key names or enum values in a PALS file matching one of the registered
    names, prefixes, or suffixes are extensions and are excluded from
    validation. Each dict maps a label to its short description.
    """

    names: dict[str, str] | None = None
    prefixes: dict[str, str] | None = None
    suffixes: dict[str, str] | None = None


class PALSroot(BaseModel):
    """Represent the root PALS structure"""

    # The standard documents `version` as a string, but the standard's own
    # examples also write bare numbers (e.g. `version: 1`).
    version: str | int | None = None

    authors: list[Author] | None = None

    notes: list[str] | None = None

    # Unlike notes, reminders are meant to be communicated to the user every
    # time the file is read.
    reminders: list[str] | None = None

    # The standard documents ANGLE_AND_ENERGY, ANGLE_AND_MOMENTUM,
    # KINETIC_AND_ENERGY, and KINETIC_AND_MOMENTUM (the default), but its
    # examples also use other values, so any string is accepted.
    phase_space_coordinates: str | None = None

    # The registered form has names/prefixes/suffixes sections; the flat
    # label -> description dict form appears in the standard's examples.
    extension_labels: ExtensionLabels | dict[str, str] | None = None

    # Files whose PALS contents combine with this one, in order, with the
    # literal entry SELF marking where this file's own contents go. Entries
    # are recorded but not yet resolved into a combined document.
    load: list[str] | None = None

    facility: Facility | None = None

    @model_validator(mode="before")
    @classmethod
    def unpack_json_structure(cls, data):
        """Deserialize the JSON/YAML/...-like dict for the root node"""
        from pals.kinds.mixin.all_element_mixin import unpack_element_items

        if not isinstance(data, dict):
            return data

        # Unwrap the `PALS` document node; per the standard, information
        # outside of it is ignored.
        if "PALS" in data:
            inner = data["PALS"]
            if not isinstance(inner, dict):
                raise TypeError(
                    f"Value for the 'PALS' root key must be a dict, but we got {inner!r}"
                )
            data = inner
        data = dict(data)

        # Authors are written as one-key `author:` dicts; unwrap them.
        if isinstance(data.get("authors"), list):
            data["authors"] = [
                entry["author"]
                if isinstance(entry, dict) and set(entry) == {"author"}
                else entry
                for entry in data["authors"]
            ]

        # Unpack each facility element's name; facility is optional.
        if data.get("facility") is not None:
            if not isinstance(data["facility"], list):
                raise TypeError("'facility' must be a list")
            data["facility"] = unpack_element_items(data["facility"], "facility")

        return data

    def model_dump(self, *args, **kwargs):
        """Custom model dump wrapping the contents in the PALS root node"""
        kwargs.setdefault("exclude_none", True)
        data = super().model_dump(*args, **kwargs)

        # Keep `version` in the output even when unset.
        data = {"version": self.version, **data}

        # Restore the one-key `author:` form of each authors entry.
        if self.authors is not None:
            data["authors"] = [
                {"author": author.model_dump(*args, **kwargs)}
                for author in self.authors
            ]

        # Reformat facility elements into their one-key named form.
        if self.facility is not None:
            data["facility"] = [elem.model_dump(**kwargs) for elem in self.facility]

        return {"PALS": data}

    @staticmethod
    def from_file(filename: str) -> Self:
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
