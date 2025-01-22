from typing import Literal

import numpy as np
from pydantic import BaseModel, Field, NonNegativeFloat, field_validator

from bayesline.api._src.registry import SettingsMenu

WeightingScheme = Literal["SqrtCap", "InvIdioVar"]


class ModelConstructionSettings(BaseModel, frozen=True, extra="forbid"):
    """
    Defines settings to build a factor risk model.
    """

    @classmethod
    def default(cls) -> "ModelConstructionSettings":
        return cls(weights="SqrtCap")

    weights: WeightingScheme = Field(
        description="The regression weights used for the factor risk model.",
        default="SqrtCap",
        examples=["SqrtCap", "InvIdioVar"],
    )
    alpha: NonNegativeFloat = Field(
        description="The ridge-shrinkage factor for the factor risk model.",
        default=0.0,
    )
    return_clip_bounds: tuple[float, float] = Field(
        description="The bounds for the return clipping.",
        default=(-0.1, 0.1),
        examples=[(-0.1, 0.1), (-np.inf, np.inf)],
    )

    @field_validator("return_clip_bounds")
    @classmethod
    def return_clip_bounds_valid(cls, v: tuple[float, float]) -> tuple[float, float]:
        lb, ub = v
        if ub < lb:
            raise ValueError(f"Lower bound {lb} cannot be bigger than upper bound {ub}")
        return v


class ModelConstructionSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """
    Defines available modelconstruction settings to build a factor risk model.
    """

    weights: list[WeightingScheme] = Field(
        description="""
        The available regression weights that can be used for the factor risk model.
        """,
    )

    def describe(self, settings: ModelConstructionSettings | None = None) -> str:
        if settings is not None:
            return f"Weights: {settings.weights}"
        else:
            return f"Weights: {', '.join(self.weights)}"

    def validate_settings(self, settings: ModelConstructionSettings) -> None:
        if settings.weights not in self.weights:
            raise ValueError(f"Invalid weights: {settings.weights}")
