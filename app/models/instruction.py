from app.extensions import db
from app.models.mixins import TimestampMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Instruction(TimestampMixin, db.Model):
    __tablename__ = "instruction"

    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer)
    description = db.Column(db.String(500))
    note_text = db.Column(db.String(500))

    recipe_links = db.relationship(
        "RecipeInstruction", back_populates="instruction", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self):
        return f"<Instruction {self.id} step={self.step}>"
