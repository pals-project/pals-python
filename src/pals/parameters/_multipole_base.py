"""Private shared base class for multipole parameter groups.

Both :class:`MagneticMultipoleParameters` and :class:`ElectricMultipoleParameters`
allow arbitrary order-indexed extra fields (e.g. ``Bn1``, ``Es3``, ``Kn0L``) and
share the same name-validation logic. This module centralizes that logic.

numpy interoperability (see pals-project/pals-python#67) is handled at the
serialization boundary in :mod:`pals.functions`, which keeps the fix general:
any numpy scalar reaching ``yaml.dump`` or ``json.dumps`` is converted to a
Python-native equivalent regardless of which model produced it.
"""

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, model_validator


def _validate_order(
    key_num: str, parameter_name: str, prefix: str, expected_format: str
) -> None:
    """Validate that the order number is a non-negative integer without leading zeros."""
    error_msg = (
        f"Invalid {parameter_name}: '{prefix}{key_num}'. "
        f"Parameter must be of the form '{expected_format}', "
        f"where 'N' is a non-negative integer without leading zeros."
    )
    if not key_num.isdigit() or (key_num.startswith("0") and key_num != "0"):
        raise ValueError(error_msg)


class _MultipoleBase(BaseModel):
    """Private shared base for multipole parameter groups.

    Subclasses must set :attr:`_PARAMETER_PREFIXES` and :attr:`_KIND_NAME`.
    Both are ``ClassVar`` and are not exposed as Pydantic fields.
    """

    # Subclasses override these:
    _PARAMETER_PREFIXES: ClassVar[dict[str, tuple[str, str]]] = {}
    _KIND_NAME: ClassVar[str] = "multipole"

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def _validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that all parameter names match the expected multipole format."""
        for key in values:
            is_length_integrated = key.endswith("L")
            base_key = key[:-1] if is_length_integrated else key

            if is_length_integrated and base_key.startswith("tilt"):
                raise ValueError(
                    f"Invalid {cls._KIND_NAME} multipole parameter: '{key}'. "
                )

            for prefix, (
                expected_format,
                description,
            ) in cls._PARAMETER_PREFIXES.items():
                if base_key.startswith(prefix):
                    key_num = base_key[len(prefix) :]
                    _validate_order(key_num, description, prefix, expected_format)
                    break
            else:
                prefix_list = ", ".join(
                    f"'{p}N'" for p in cls._PARAMETER_PREFIXES if p != "tilt"
                )
                raise ValueError(
                    f"Invalid {cls._KIND_NAME} multipole parameter: '{key}'. "
                    f"Parameters must be of the form 'tiltN', {prefix_list} "
                    f"(with optional 'L' suffix for length-integrated), "
                    f"where 'N' is a non-negative integer."
                )

        return values
