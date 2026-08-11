from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe_appliance import RecipeAppliance


class Appliance(TimestampMixin, db.Model):
    __tablename__ = "appliance"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    recipe_links: Mapped[list[RecipeAppliance]] = relationship(
        "RecipeAppliance", back_populates="appliance", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self) -> str:
        return f"<Appliance {self.id} {self.name!r}>"
