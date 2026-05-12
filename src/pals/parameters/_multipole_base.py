"""Private shared base class for multipole parameter groups.

Both :class:`MagneticMultipoleParameters` and :class:`ElectricMultipoleParameters`
allow arbitrary order-indexed extra fields (e.g. ``Bn1``, ``Es3``, ``Kn0L``).
Because these fields are not declared with a type, Pydantic would otherwise
store them as-is, preserving non-native numeric inputs like ``numpy.float64``.
That breaks downstream YAML serialization (PyYAML emits unsafe Python-object
tags for numpy scalars). See pals-project/pals-python#67.

This module centralizes the name-validation logic and adds numpy-to-native
coercion at construction time.
"""

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, model_validator


def _coerce_numpy_value(value: Any) -> Any:
    """Convert numpy scalars/arrays to Python-native equivalents.

    Recurses through ``list``/``tuple``/``dict`` containers so nested
    structures are also cleaned. Returns ``value`` unchanged when numpy is
    not installed or the value is not a numpy type. numpy remains an optional
    dependency of this project.
    """
    try:
        import numpy as np
    except ImportError:
        return value

    if isinstance(value, np.ndarray):
        if value.ndim == 0:
            return value.item()
        return _coerce_numpy_value(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, list):
        return [_coerce_numpy_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_coerce_numpy_value(v) for v in value)
    if isinstance(value, dict):
        return {k: _coerce_numpy_value(v) for k, v in value.items()}
    return value


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
    def _validate_and_coerce(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate parameter names and coerce numpy values to Python natives."""
        coerced: dict[str, Any] = {}
        for key, value in values.items():
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

            coerced[key] = _coerce_numpy_value(value)

        return coerced
