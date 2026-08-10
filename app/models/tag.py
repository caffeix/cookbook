from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin
from app.utils import slugify

if TYPE_CHECKING:
    from app.models.recipe_tag import RecipeTag


class Tag(TimestampMixin, db.Model):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("slug", name="uq_tag_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(110), nullable=False, server_default="")

    recipe_links: Mapped[list[RecipeTag]] = relationship(
        "RecipeTag", back_populates="tag", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self) -> str:
        return f"<Tag {self.id} {self.name!r}>"


@event.listens_for(Tag, "before_insert")
@event.listens_for(Tag, "before_update")
def _set_tag_slug(mapper, connection, target: Tag) -> None:
    """Auto-generate slug from name before insert/update."""
    if target.name and not target.slug:
        target.slug = slugify(target.name)
