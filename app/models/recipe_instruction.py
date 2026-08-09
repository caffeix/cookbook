from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeInstruction(TimestampMixin, db.Model):
    __tablename__ = "recipe_instruction"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    instruction_id = db.Column(
        db.Integer, db.ForeignKey("instruction.id"), primary_key=True
    )

    recipe = db.relationship("Recipe", back_populates="instruction_links")
    instruction = db.relationship("Instruction", back_populates="recipe_links")
