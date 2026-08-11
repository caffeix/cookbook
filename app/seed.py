import click
from flask import Blueprint
from .extensions import db
from .models import (
    Recipe, Ingredient, RecipeIngredient,
    Tag, RecipeTag,
    Category, RecipeCategory,
    Replaceable, Appliance, 
    Utensil, RecipeAppliance,
    RecipeUtensil, Instruction, RecipeInstruction
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

    italian_category = Category(name="Italian", slug=slugify("Italian"))

    recipe = Recipe(
        title="Garlic Pasta",
        description="A simple, flavour-packed weeknight pasta ready in under 20 minutes.",
        picture="uploads/garlic_pasta.jpg",
        cook_time=20,
        difficulty="easy",
    )

    pancake_recipe = Recipe(
        title="Fluffy Pancakes",
        description="Classic homemade golden pancakes perfect for breakfast.",
        picture="uploads/pancakes.jpg",
        cook_time=15,
        difficulty="easy",
    )

    tacos_recipe = Recipe(
        title="Crispy Beef Tacos",
        description="Savory spiced ground beef filled into crispy tortilla shells with fresh toppings.",
        picture="uploads/tacos.jpg",
        cook_time=25,
        difficulty="medium",
    )

    flour = Ingredient(name="Flour", slug=slugify("Flour"))
    milk = Ingredient(name="Milk", slug=slugify("Milk"))
    oat_milk = Ingredient(name="Oat Milk", slug=slugify("Oat Milk"))
    egg = Ingredient(name="Egg", slug=slugify("Egg"))
    ground_beef = Ingredient(name="Ground Beef", slug=slugify("Ground Beef"))
    taco_shell = Ingredient(name="Taco Shell", slug=slugify("Taco Shell"))
    cheddar = Ingredient(name="Cheddar Cheese", slug=slugify("Cheddar Cheese"))

    breakfast_tag = Tag(name="Breakfast", slug=slugify("Breakfast"))
    dinner_tag = Tag(name="Dinner", slug=slugify("Dinner"))

    american_category = Category(name="American", slug=slugify("American"))
    mexican_category = Category(name="Mexican", slug=slugify("Mexican"))

    pasta_inst1 = Instruction(step=1, description="Boil spaghetti in salted water until al dente.", note_text="Save 1/2 cup of pasta water before draining.")
    pasta_inst2 = Instruction(step=2, description="Sauté minced garlic in olive oil over medium heat until fragrant.", note_text="Be careful not to burn the garlic.")
    pasta_inst3 = Instruction(step=3, description="Toss drained pasta with garlic oil and pasta water.", note_text="Season with salt and pepper to taste.")
    inst1 = Instruction(step=1, description="Whisk flour, milk, and eggs in a bowl until smooth.", note_text="Do not overmix to keep pancakes fluffy.")
    inst2 = Instruction(step=2, description="Pour batter onto a hot frying pan and cook until golden on both sides.", note_text="Flip when bubbles form.")
    inst3 = Instruction(step=3, description="Brown the beef in a pan with seasonings.", note_text="Drain excess fat if needed.")
    inst4 = Instruction(step=4, description="Fill taco shells with beef and top with shredded cheddar.", note_text="Serve hot with fresh salsa.")

    air_fryer = Appliance(name="Air Fryer")
    whisk = Utensil(name="Whisk")
    small_pot = Utensil(name="Small pot")
    frying_pan = Appliance(name="Frying pan")
    spatula = Utensil(name="Spatula")
    stovetop = Appliance(name="Stovetop")

    db.session.add_all([
        garlic, olive_oil, spaghetti, fusilli, flour, milk, oat_milk, egg, ground_beef, taco_shell, cheddar,
        breakfast_tag, dinner_tag,
        italian_category, american_category, mexican_category,
        recipe, pancake_recipe, tacos_recipe,
        air_fryer, whisk, small_pot, frying_pan, spatula, stovetop,
        pasta_inst1, pasta_inst2, pasta_inst3, inst1, inst2, inst3, inst4
    ])
    db.session.flush()  # assigns IDs before referencing them

    db.session.add_all([
        # Recipe 1: Garlic Pasta
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=garlic.id, quantity="2", unit="cloves"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=olive_oil.id, quantity="2", unit="tbsp"),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=spaghetti.id, quantity="200", unit="g"),
        RecipeCategory(recipe_id=recipe.id, category_id=italian_category.id),
        RecipeInstruction(recipe_id=recipe.id, instruction_id=pasta_inst1.id),
        RecipeInstruction(recipe_id=recipe.id, instruction_id=pasta_inst2.id),
        RecipeInstruction(recipe_id=recipe.id, instruction_id=pasta_inst3.id),
        Replaceable(
            recipe_id=recipe.id,
            original_ingredient_id=spaghetti.id,
            swap_ingredient_id=fusilli.id,
        ),
        RecipeUtensil(recipe_id=recipe.id, utensil_id=small_pot.id),
        RecipeAppliance(recipe_id=recipe.id, appliance_id=frying_pan.id),

        # Recipe 2: Fluffy Pancakes
        RecipeIngredient(recipe_id=pancake_recipe.id, ingredient_id=flour.id, quantity="1", unit="cup"),
        RecipeIngredient(recipe_id=pancake_recipe.id, ingredient_id=milk.id, quantity="1", unit="cup"),
        RecipeIngredient(recipe_id=pancake_recipe.id, ingredient_id=egg.id, quantity="1", unit="piece"),
        RecipeTag(recipe_id=pancake_recipe.id, tag_id=breakfast_tag.id),
        RecipeCategory(recipe_id=pancake_recipe.id, category_id=american_category.id),
        RecipeInstruction(recipe_id=pancake_recipe.id, instruction_id=inst1.id),
        RecipeInstruction(recipe_id=pancake_recipe.id, instruction_id=inst2.id),
        Replaceable(
            recipe_id=pancake_recipe.id,
            original_ingredient_id=milk.id,
            swap_ingredient_id=oat_milk.id,
        ),
        RecipeUtensil(recipe_id=pancake_recipe.id, utensil_id=whisk.id),
        RecipeUtensil(recipe_id=pancake_recipe.id, utensil_id=spatula.id),
        RecipeAppliance(recipe_id=pancake_recipe.id, appliance_id=frying_pan.id),

        # Recipe 3: Crispy Beef Tacos
        RecipeIngredient(recipe_id=tacos_recipe.id, ingredient_id=ground_beef.id, quantity="300", unit="g"),
        RecipeIngredient(recipe_id=tacos_recipe.id, ingredient_id=taco_shell.id, quantity="4", unit="shells"),
        RecipeIngredient(recipe_id=tacos_recipe.id, ingredient_id=cheddar.id, quantity="50", unit="g"),
        RecipeTag(recipe_id=tacos_recipe.id, tag_id=dinner_tag.id),
        RecipeCategory(recipe_id=tacos_recipe.id, category_id=mexican_category.id),
        RecipeInstruction(recipe_id=tacos_recipe.id, instruction_id=inst3.id),
        RecipeInstruction(recipe_id=tacos_recipe.id, instruction_id=inst4.id),
        RecipeUtensil(recipe_id=tacos_recipe.id, utensil_id=spatula.id),
        RecipeAppliance(recipe_id=tacos_recipe.id, appliance_id=stovetop.id),
    ])

    db.session.commit()
    click.echo(
        f"Seeded {len(db.session.scalars(db.select(Recipe)).all())} recipes, "
        f"{len(db.session.scalars(db.select(Ingredient)).all())} ingredients, "
        f"{len(db.session.scalars(db.select(Tag)).all())} tags, "
        f"{len(db.session.scalars(db.select(Category)).all())} categories."
    )