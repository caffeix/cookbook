from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.instruction import Instruction


class RecipeInstruction(TimestampMixin, db.Model):
    __tablename__ = "recipe_instruction"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    instruction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("instruction.id"), primary_key=True
    )

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="instruction_links")
    instruction: Mapped[Instruction] = relationship(
        "Instruction", back_populates="recipe_links"
    )
