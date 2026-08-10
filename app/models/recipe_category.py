from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.category import Category


class RecipeCategory(TimestampMixin, db.Model):
    __tablename__ = "recipe_category"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), primary_key=True
    )

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="category_links")
    category: Mapped[Category] = relationship(
        "Category", back_populates="recipe_links"
    )
