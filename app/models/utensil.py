from app.extensions import db
from app.models.mixins import TimestampMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Utensil(TimestampMixin, db.Model):
    __tablename__ = "utensil"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(255))

    recipe_links = db.relationship(
        "RecipeUtensil", back_populates="utensil", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self):
        return f"<Utensil {self.id} {self.name!r}>"
