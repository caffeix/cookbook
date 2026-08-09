from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeUtensil(TimestampMixin, db.Model):
    __tablename__ = "recipe_utensil"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    utensil_id = db.Column(db.Integer, db.ForeignKey("utensil.id"), primary_key=True)

    recipe = db.relationship("Recipe", back_populates="utensil_links")
    utensil = db.relationship("Utensil", back_populates="recipe_links")
