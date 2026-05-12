from typing import ClassVar

from pals.parameters._multipole_base import _MultipoleBase


class ElectricMultipoleParameters(_MultipoleBase):
    """Electric multipole parameters

    Valid parameter formats:
    - tiltN: Tilt of Nth order multipole
    - EnN: Normal component of Nth order multipole
    - EsN: Skew component of Nth order multipole
    - *NL: Length-integrated versions of components (e.g., En3L, EsNL)

    Where N is a positive integer without leading zeros (except "0" itself).
    """

    _KIND_NAME: ClassVar[str] = "electric"
    _PARAMETER_PREFIXES: ClassVar[dict[str, tuple[str, str]]] = {
        "tilt": ("tiltN", "Tilt"),
        "En": ("EnN", "Normal component"),
        "Es": ("EsN", "Skew component"),
    }
