import builtins

from annotated_types import Ge
from typing import Annotated, Literal
from pydantic import BaseModel, Field, field_validator


class Vertex(BaseModel):
    point: tuple[float, float]
    radius: float | tuple[float, float] | None = None
    convex: bool = True
    tilt: float = 0


class Vertices(BaseModel):
    center: tuple[float, float] = Field(default=(0, 0))
    absolute_vertices: bool = False
    list: builtins.list[Vertex] = Field(default_factory=builtins.list)


class ApertureParameters(BaseModel):
    """Aperture parameters"""

    @field_validator("x_limits", "y_limits")
    @classmethod
    def validate_limits(cls, v):
        """Validate that limits are None or that min < max"""
        if v[0] is not None and v[1] is not None and v[0] >= v[1]:
            raise ValueError("Lower limit must be less than upper limit")
        return v

    x_limits: list[float | None, float | None] = Field(default=[None, None])
    y_limits: list[float | None, float | None] = Field(default=[None, None])
    shape: Literal["RECTANGULAR", "ELLIPTICAL", "VERTICES", "CUSTOM_SHAPE"] = (
        "RECTANGULAR"
    )
    location: Literal[
        "ENTRANCE_END", "CENTER", "EXIT_END", "BOTH_ENDS", "NOWHERE", "EVERYWHERE"
    ] = "ENTRANCE_END"
    material: str = ""
    thickness: Annotated[float, Ge(0.0)] = 0.0
    aperture_shifts_with_body: bool = False
    aperture_active: bool = True
    vertices: Vertices | None = None
