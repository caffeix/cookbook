from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin
from app.utils import slugify

if TYPE_CHECKING:
    from app.models.recipe_ingredient import RecipeIngredient


class Ingredient(TimestampMixin, db.Model):
    __tablename__ = "ingredient"
    __table_args__ = (UniqueConstraint("slug", name="uq_ingredient_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(170), nullable=False, server_default="")

    recipe_links: Mapped[list[RecipeIngredient]] = relationship(
        "RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self) -> str:
        return f"<Ingredient {self.id} {self.name!r}>"


@event.listens_for(Ingredient, "before_insert")
@event.listens_for(Ingredient, "before_update")
def _set_ingredient_slug(mapper, connection, target: Ingredient) -> None:
    """Auto-generate slug from name before insert/update."""
    if target.name and not target.slug:
        target.slug = slugify(target.name)
