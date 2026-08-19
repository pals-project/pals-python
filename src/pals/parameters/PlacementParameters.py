from typing import Literal, Optional, TypeAlias

from pydantic import BaseModel, Field


ReferencePoint: TypeAlias = Literal["ENTRANCE_END", "CENTER", "EXIT_END", "ZERO_POINT"]


class PlacementParameters(BaseModel):
    offset: float = Field(
        default=0.0,
        description="Real [m]. Longitudinal offset of the line item. Default is zero.",
        allow_inf_nan=False,
    )

    to_point: ReferencePoint = Field(
        default="ENTRANCE_END",
        description="Line item offset end point. Default is ENTRANCE_END.",
    )

    base_item: Optional[str] = Field(
        default=None, description="Line item containing the `from_point`."
    )

    from_point: ReferencePoint = Field(
        default="EXIT_END",
        description="Base line item offset beginning point. Default is EXIT_END.",
    )
