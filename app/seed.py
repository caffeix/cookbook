import click
from flask import Blueprint
from .extensions import db
from .models import (
    Recipe, Ingredient, RecipeIngredient,
    Tag, RecipeTag,
    Category, RecipeCategory,
    Replaceable,
)
from .utils import slugify

seed_bp = Blueprint("seed", __name__)

@seed_bp.cli.command("run")
def seed():
    """Populate the database with sample data for local development."""
    if db.session.execute(db.select(Recipe)).scalars().first():
        click.echo("Database already has data — skipping seed.")
        return

    garlic = Ingredient(name="Garlic", slug=slugify("Garlic"))
    olive_oil = Ingredient(name="Olive Oil", slug=slugify("Olive Oil"))
    spaghetti = Ingredient(name="Spaghetti", slug=slugify("Spaghetti"))
    fusilli = Ingredient(name="Fusilli", slug=slugify("Fusilli"))

    italian_tag = Tag(name="Italian", slug=slugify("Italian"))
    quick_tag = Tag(name="Quick Meals", slug=slugify("Quick Meals"))

    italian_category = Category(name="Italian", slug=slugify("Italian"))

    recipe = Recipe(
        title="Garlic Pasta",
        description="A simple, flavour-packed weeknight pasta ready in under 20 minutes.",
        cook_time=20,
        difficulty="easy",
    )

    db.session.add_all([
        garlic, olive_oil, spaghetti, fusilli,
        italian_tag, quick_tag, italian_category, recipe,
    ])
    db.session.flush()  # assigns IDs before referencing them

    db.session.add_all([
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=garlic.id, quantity="2", unit="cloves"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=olive_oil.id, quantity="2", unit="tbsp"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=spaghetti.id, quantity="200", unit="g"),
        RecipeTag(recipe_id=recipe.id, tag_id=italian_tag.id),
        RecipeTag(recipe_id=recipe.id, tag_id=quick_tag.id),
        RecipeCategory(recipe_id=recipe.id, category_id=italian_category.id),
        Replaceable(
            recipe_id=recipe.id,
            original_ingredient_id=spaghetti.id,
            swap_ingredient_id=fusilli.id,
        ),
    ])

    db.session.commit()
    click.echo(
        f"Seeded 1 recipe, "
        f"{db.session.execute(db.select(Ingredient)).scalars().count()} ingredients, "
        f"{db.session.execute(db.select(Tag)).scalars().count()} tags, "
        f"{db.session.execute(db.select(Category)).scalars().count()} categories."
    )