from app.extensions import db
from app.models.mixins import TimestampMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Recipe(TimestampMixin, db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.String(255))
    cook_time = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))

    # association-object relationships (gives access to the join row itself,
    # e.g. recipe.ingredient_links[0].quantity)
    ingredient_links = db.relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    category_links = db.relationship(
        "RecipeCategory", back_populates="recipe", cascade="all, delete-orphan"
    )
    tag_links = db.relationship(
        "RecipeTag", back_populates="recipe", cascade="all, delete-orphan"
    )
    instruction_links = db.relationship(
        "RecipeInstruction", back_populates="recipe", cascade="all, delete-orphan"
    )
    appliance_links = db.relationship(
        "RecipeAppliance", back_populates="recipe", cascade="all, delete-orphan"
    )
    utensil_links = db.relationship(
        "RecipeUtensil", back_populates="recipe", cascade="all, delete-orphan"
    )
    replaceables = db.relationship(
        "Replaceable",
        back_populates="recipe",
        cascade="all, delete-orphan",
        foreign_keys="Replaceable.recipe_id",
    )

    # convenience proxies straight to the related objects, e.g. recipe.ingredients
    ingredients = association_proxy("ingredient_links", "ingredient")
    categories = association_proxy("category_links", "category")
    tags = association_proxy("tag_links", "tag")
    instructions = association_proxy("instruction_links", "instruction")
    appliances = association_proxy("appliance_links", "appliance")
    utensils = association_proxy("utensil_links", "utensil")

    def __repr__(self):
        return f"<Recipe {self.id} {self.title!r}>"
