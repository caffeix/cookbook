from app.extensions import db
from app.models.mixins import TimestampMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Category(TimestampMixin, db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(255))

    recipe_links = db.relationship(
        "RecipeCategory", back_populates="category", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self):
        return f"<Category {self.id} {self.name!r}>"
