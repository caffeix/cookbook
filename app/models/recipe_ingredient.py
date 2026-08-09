from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeIngredient(TimestampMixin, db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), primary_key=True
    )
    quantity = db.Column(db.String(50))
    unit = db.Column(db.String(20))

    recipe = db.relationship("Recipe", back_populates="ingredient_links")
    ingredient = db.relationship("Ingredient", back_populates="recipe_links")
