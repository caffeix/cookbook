from app.extensions import db
from app.models.mixins import TimestampMixin


class RecipeAppliance(TimestampMixin, db.Model):
    __tablename__ = "recipe_appliance"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    appliance_id = db.Column(
        db.Integer, db.ForeignKey("appliance.id"), primary_key=True
    )

    recipe = db.relationship("Recipe", back_populates="appliance_links")
    appliance = db.relationship("Appliance", back_populates="recipe_links")
