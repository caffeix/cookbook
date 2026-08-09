from app.extensions import db
from app.models.mixins import TimestampMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Tag(TimestampMixin, db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    recipe_links = db.relationship(
        "RecipeTag", back_populates="tag", cascade="all, delete-orphan"
    )
    recipes = association_proxy("recipe_links", "recipe")

    def __repr__(self):
        return f"<Tag {self.id} {self.name!r}>"
