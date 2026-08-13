from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient


class IngredientRole(str, enum.Enum):
    MAIN = "Main"
    ESSENTIAL = "Essential"
    OPTIONAL = "Optional"


class RecipeIngredient(TimestampMixin, db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ingredient.id"), primary_key=True
    )
    quantity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role: Mapped[Optional[IngredientRole]] = mapped_column(
        Enum(IngredientRole, name="ingredient_role", native_enum=False), nullable=True
    )

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="ingredient_links")
    ingredient: Mapped[Ingredient] = relationship(
        "Ingredient", back_populates="recipe_links"
    )
