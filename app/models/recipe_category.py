from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeCategory(TimestampMixin, db.Model):
    __tablename__ = "recipe_category"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), primary_key=True
    )

    recipe = db.relationship("Recipe", back_populates="category_links")
    category = db.relationship("Category", back_populates="recipe_links")
