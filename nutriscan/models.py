
from typing import Literal

from pydantic import BaseModel, Field


class NutritionRow(BaseModel):
    """Validated data for one nutrition-table row."""

    nutrient: str | None = None

    value: float | None = Field(
        default=None,
        ge=0,
        description="Nutrient value; cannot be negative"
    )

    unit: Literal["kcal", "g", "mg", "ml"] | None = None

    rda_percent: float | None = Field(
        default=None,
        ge=0,
        description="Percentage of recommended daily allowance"
    )
