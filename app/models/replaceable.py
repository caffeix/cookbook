from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient


class Replaceable(TimestampMixin, db.Model):
    __tablename__ = "replaceable"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), nullable=False
    )
    original_ingredient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ingredient.id"), nullable=False
    )
    swap_ingredient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ingredient.id"), nullable=False
    )

    recipe: Mapped[Recipe] = relationship(
        "Recipe",
        back_populates="replaceables",
        foreign_keys=[recipe_id],
    )
    original_ingredient: Mapped[Ingredient] = relationship(
        "Ingredient",
        foreign_keys=[original_ingredient_id],
    )
    swap_ingredient: Mapped[Ingredient] = relationship(
        "Ingredient",
        foreign_keys=[swap_ingredient_id],
    )

    def __repr__(self) -> str:
        return f"<Replaceable {self.id} recipe={self.recipe_id}>"
