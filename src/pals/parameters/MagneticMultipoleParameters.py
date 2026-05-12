from pydantic import BaseModel, ConfigDict, model_validator
from typing import Any

# Valid parameter prefixes, their expected format and description
_PARAMETER_PREFIXES = {
    "tilt": ("tiltN", "Tilt"),
    "Bn": ("BnN", "Normal component"),
    "Bs": ("BsN", "Skew component"),
    "Kn": ("KnN", "Normalized normal component"),
    "Ks": ("KsN", "Normalized skew component"),
}


def _validate_order(
    key_num: str, parameter_name: str, prefix: str, expected_format: str
) -> None:
    """Validate that the order number is a non-negative integer without leading zeros."""
    error_msg = (
        f"Invalid {parameter_name}: '{prefix}{key_num}'. "
        f"Parameter must be of the form '{expected_format}', where 'N' is a non-negative integer without leading zeros."
    )
    if not key_num.isdigit() or (key_num.startswith("0") and key_num != "0"):
        raise ValueError(error_msg)


class MagneticMultipoleParameters(BaseModel):
    """Magnetic multipole parameters

    Valid parameter formats:
    - tiltN: Tilt of Nth order multipole
    - BnN: Normal component of Nth order multipole
    - BsN: Skew component of Nth order multipole
    - KnN: Normalized normal component of Nth order multipole
    - KsN: Normalized skew component of Nth order multipole
    - *NL: Length-integrated versions of components (e.g., Bn3L, KsNL)

    Where N is a positive integer without leading zeros (except "0" itself).
    """

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate all parameter names match the expected multipole format."""
        for key in values:
            # Check if key ends with 'L' for length-integrated values
            is_length_integrated = key.endswith("L")
            base_key = key[:-1] if is_length_integrated else key

            # No length-integrated values allowed for tilt parameter
            if is_length_integrated and base_key.startswith("tilt"):
                raise ValueError(f"Invalid magnetic multipole parameter: '{key}'. ")

            # Find matching prefix
            for prefix, (expected_format, description) in _PARAMETER_PREFIXES.items():
                if base_key.startswith(prefix):
                    key_num = base_key[len(prefix) :]
                    _validate_order(key_num, description, prefix, expected_format)
                    break
            else:
                raise ValueError(
                    f"Invalid magnetic multipole parameter: '{key}'. "
                    f"Parameters must be of the form 'tiltN', 'BnN', 'BsN', 'KnN', or 'KsN' "
                    f"(with optional 'L' suffix for length-integrated), where 'N' is a non-negative integer."
                )
        return values
