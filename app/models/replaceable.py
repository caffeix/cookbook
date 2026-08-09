from app.extensions import db
from app.models.mixins import TimestampMixin


class Replaceable(TimestampMixin, db.Model):
    __tablename__ = "replaceable"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    original_ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), nullable=False
    )
    swap_ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredient.id"), nullable=False
    )

    recipe = db.relationship(
        "Recipe", back_populates="replaceables", foreign_keys=[recipe_id]
    )
    original_ingredient = db.relationship(
        "Ingredient", foreign_keys=[original_ingredient_id]
    )
    swap_ingredient = db.relationship("Ingredient", foreign_keys=[swap_ingredient_id])

    def __repr__(self):
        return f"<Replaceable {self.id} recipe={self.recipe_id}>"
