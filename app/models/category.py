from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Text, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin
from app.utils import slugify

if TYPE_CHECKING:
    from app.models.recipe_category import RecipeCategory


class Category(TimestampMixin, db.Model):
    __tablename__ = "category"
    __table_args__ = (UniqueConstraint("slug", name="uq_category_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, server_default="")
    icon: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    recipe_links: Mapped[list[RecipeCategory]] = relationship(
        "RecipeCategory", back_populates="category", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self) -> str:
        return f"<Category {self.id} {self.name!r}>"


@event.listens_for(Category, "before_insert")
@event.listens_for(Category, "before_update")
def _set_category_slug(mapper, connection, target: Category) -> None:
    """Auto-generate slug from name before insert/update."""
    if target.name and not target.slug:
        target.slug = slugify(target.name)
