from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.extensions import db
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.recipe_ingredient import RecipeIngredient
    from app.models.recipe_category import RecipeCategory
    from app.models.recipe_tag import RecipeTag
    from app.models.recipe_instruction import RecipeInstruction
    from app.models.recipe_appliance import RecipeAppliance
    from app.models.recipe_utensil import RecipeUtensil
    from app.models.replaceable import Replaceable


class Recipe(TimestampMixin, db.Model):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Stored as a relative path under static/uploads/, e.g. "uploads/pasta.jpg"
    picture: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cook_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Association-object relationships (exposes the join row for extra columns)
    ingredient_links: Mapped[list[RecipeIngredient]] = relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    category_links: Mapped[list[RecipeCategory]] = relationship(
        "RecipeCategory", back_populates="recipe", cascade="all, delete-orphan"
    )
    tag_links: Mapped[list[RecipeTag]] = relationship(
        "RecipeTag", back_populates="recipe", cascade="all, delete-orphan"
    )
    instruction_links: Mapped[list[RecipeInstruction]] = relationship(
        "RecipeInstruction", back_populates="recipe", cascade="all, delete-orphan"
    )
    appliance_links: Mapped[list[RecipeAppliance]] = relationship(
        "RecipeAppliance", back_populates="recipe", cascade="all, delete-orphan"
    )
    utensil_links: Mapped[list[RecipeUtensil]] = relationship(
        "RecipeUtensil", back_populates="recipe", cascade="all, delete-orphan"
    )
    replaceables: Mapped[list[Replaceable]] = relationship(
        "Replaceable",
        back_populates="recipe",
        cascade="all, delete-orphan",
        foreign_keys="Replaceable.recipe_id",
    )

    # Convenience proxies straight to the related objects, e.g. recipe.tags
    ingredients = association_proxy("ingredient_links", "ingredient")
    categories = association_proxy("category_links", "category")
    tags = association_proxy("tag_links", "tag")
    instructions = association_proxy("instruction_links", "instruction")
    appliances = association_proxy("appliance_links", "appliance")
    utensils = association_proxy("utensil_links", "utensil")

    def __repr__(self) -> str:
        return f"<Recipe {self.id} {self.title!r}>"
