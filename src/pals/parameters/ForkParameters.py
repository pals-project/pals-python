from typing import Literal

from pydantic import BaseModel


class ForkParameters(BaseModel):
    """Fork parameters"""

    to_line: str = ""
    to_ele: str = ""
    direction: Literal["FORWARDS", "BACKWARDS"] = "FORWARDS"
    propagate_reference: bool = True
