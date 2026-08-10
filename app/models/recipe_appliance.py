from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.appliance import Appliance


class RecipeAppliance(TimestampMixin, db.Model):
    __tablename__ = "recipe_appliance"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    appliance_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("appliance.id"), primary_key=True
    )

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="appliance_links")
    appliance: Mapped[Appliance] = relationship(
        "Appliance", back_populates="recipe_links"
    )
