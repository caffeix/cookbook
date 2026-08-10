from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe_instruction import RecipeInstruction


class Instruction(TimestampMixin, db.Model):
    __tablename__ = "instruction"

    id: Mapped[int] = mapped_column(primary_key=True)
    step: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    note_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    recipe_links: Mapped[list[RecipeInstruction]] = relationship(
        "RecipeInstruction", back_populates="instruction", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self) -> str:
        return f"<Instruction {self.id} step={self.step}>"
