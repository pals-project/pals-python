from typing import ClassVar

from pals.parameters._multipole_base import _MultipoleBase


class MagneticMultipoleParameters(_MultipoleBase):
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

    _KIND_NAME: ClassVar[str] = "magnetic"
    _PARAMETER_PREFIXES: ClassVar[dict[str, tuple[str, str]]] = {
        "tilt": ("tiltN", "Tilt"),
        "Bn": ("BnN", "Normal component"),
        "Bs": ("BsN", "Skew component"),
        "Kn": ("KnN", "Normalized normal component"),
        "Ks": ("KsN", "Normalized skew component"),
    }
