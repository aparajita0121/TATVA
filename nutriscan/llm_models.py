
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NutritionValue(BaseModel):
    """One extracted nutrient value with its measurement basis."""

    value: float | None = Field(default=None, ge=0)

    unit: Literal["kcal", "g", "mg", "ml"] | None = None

    basis: Literal[
        "per_100g",
        "per_100ml",
        "per_serving",
        "unknown"
    ] = "unknown"


class ExtractedNutrition(BaseModel):
    """Structured nutrition data returned by the LLM."""

    model_config = ConfigDict(extra="forbid")

    product_name: str | None = None
    serving_size: str | None = None

    energy: NutritionValue = Field(default_factory=NutritionValue)
    protein: NutritionValue = Field(default_factory=NutritionValue)
    carbohydrates: NutritionValue = Field(default_factory=NutritionValue)
    total_sugars: NutritionValue = Field(default_factory=NutritionValue)
    total_fat: NutritionValue = Field(default_factory=NutritionValue)
    saturated_fat: NutritionValue = Field(default_factory=NutritionValue)
    sodium: NutritionValue = Field(default_factory=NutritionValue)
