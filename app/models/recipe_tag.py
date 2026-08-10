from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.tag import Tag


class RecipeTag(TimestampMixin, db.Model):
    __tablename__ = "recipe_tag"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tag.id"), primary_key=True
    )

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="tag_links")
    tag: Mapped[Tag] = relationship("Tag", back_populates="recipe_links")
