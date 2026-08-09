import click
from flask import Blueprint
from .extensions import db
from .models import (
    Recipe, Ingredient, RecipeIngredient,
    Tag, RecipeTag,
    Category, RecipeCategory,
    Replaceable,
)

seed_bp = Blueprint("seed", __name__)

@seed_bp.cli.command("run")
def seed():
    """Populate the database with sample data for local development."""
    if Recipe.query.first():
        click.echo("Database already has data — skipping seed.")
        return

    garlic = Ingredient(name="Garlic")
    olive_oil = Ingredient(name="Olive oil")
    spaghetti = Ingredient(name="Spaghetti")
    fusilli = Ingredient(name="Fusilli")

    italian_tag = Tag(name="Italian")
    italian_category = Category(name="Italian")  # adjust field name if different

    recipe = Recipe(title="Garlic Pasta", description="Simple weeknight pasta")

    db.session.add_all([
        garlic, olive_oil, spaghetti, fusilli,
        italian_tag, italian_category, recipe,
    ])
    db.session.flush()  # assigns IDs before we reference them below

    db.session.add_all([
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=garlic.id, quantity="2", unit="cloves"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=olive_oil.id, quantity="2", unit="tbsp"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=spaghetti.id, quantity="200", unit="g"),
        RecipeTag(recipe_id=recipe.id, tag_id=italian_tag.id),
        RecipeCategory(recipe_id=recipe.id, category_id=italian_category.id),  # adjust field names if different
        Replaceable(
            recipe_id=recipe.id,
            original_ingredient_id=spaghetti.id,
            swap_ingredient_id=fusilli.id,
        ),
    ])

    db.session.commit()
    click.echo(
        f"Seeded 1 recipe, {Ingredient.query.count()} ingredients, "
        f"{Tag.query.count()} tags, {Category.query.count()} categories, "
        f"{Replaceable.query.count()} replaceable(s)."
    )