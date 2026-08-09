from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeTag(TimestampMixin, db.Model):
    __tablename__ = "recipe_tag"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)

    recipe = db.relationship("Recipe", back_populates="tag_links")
    tag = db.relationship("Tag", back_populates="recipe_links")
