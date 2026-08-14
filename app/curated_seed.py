"""
Curated recipe seed script.

Adds 8 simple, low-effort recipes to the recipe list.
"""

import click
from flask import Blueprint

from .extensions import db
from .models import (
    Recipe, Ingredient, RecipeIngredient, IngredientRole,
    Tag, RecipeTag,
    Category, RecipeCategory,
    Replaceable, Appliance,
    Utensil, RecipeAppliance,
    RecipeUtensil, Instruction, RecipeInstruction,
    Difficulty,
)
from .utils import slugify

curated_seed_bp = Blueprint("curated_seed", __name__)


# ---------------------------------------------------------------------------
# get-or-create helpers (cached per run to avoid repeat queries)
# ---------------------------------------------------------------------------

class Registry:
    """Small in-memory cache over get-or-create lookups for one seed run."""

    def __init__(self):
        self._ingredients = {}
        self._tags = {}
        self._categories = {}
        self._appliances = {}
        self._utensils = {}

    def ingredient(self, name):
        slug = slugify(name)
        if slug in self._ingredients:
            return self._ingredients[slug]
        obj = db.session.execute(
            db.select(Ingredient).where(Ingredient.slug == slug)
        ).scalar_one_or_none()
        if obj is None:
            obj = Ingredient(name=name, slug=slug)
            db.session.add(obj)
            db.session.flush()
        self._ingredients[slug] = obj
        return obj

    def tag(self, name):
        slug = slugify(name)
        if slug in self._tags:
            return self._tags[slug]
        obj = db.session.execute(
            db.select(Tag).where(Tag.slug == slug)
        ).scalar_one_or_none()
        if obj is None:
            obj = Tag(name=name, slug=slug)
            db.session.add(obj)
            db.session.flush()
        self._tags[slug] = obj
        return obj

    def category(self, name):
        slug = slugify(name)
        if slug in self._categories:
            return self._categories[slug]
        obj = db.session.execute(
            db.select(Category).where(Category.slug == slug)
        ).scalar_one_or_none()
        if obj is None:
            obj = Category(name=name, slug=slug)
            db.session.add(obj)
            db.session.flush()
        self._categories[slug] = obj
        return obj

    def appliance(self, name, icon=None):
        if name in self._appliances:
            return self._appliances[name]
        obj = db.session.execute(
            db.select(Appliance).where(Appliance.name == name)
        ).scalar_one_or_none()
        if obj is None:
            obj = Appliance(name=name, icon=icon)
            db.session.add(obj)
            db.session.flush()
        self._appliances[name] = obj
        return obj

    def utensil(self, name, icon=None):
        if name in self._utensils:
            return self._utensils[name]
        obj = db.session.execute(
            db.select(Utensil).where(Utensil.name == name)
        ).scalar_one_or_none()
        if obj is None:
            obj = Utensil(name=name, icon=icon)
            db.session.add(obj)
            db.session.flush()
        self._utensils[name] = obj
        return obj


def _add_ingredient(reg, recipe, name, quantity, unit, role):
    ing = reg.ingredient(name)
    db.session.add(
        RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ing.id,
            quantity=quantity,
            unit=unit,
            role=role,
        )
    )
    return ing


def _add_swap(reg, recipe, original_ing, swap_name):
    swap_ing = reg.ingredient(swap_name)
    db.session.add(
        Replaceable(
            recipe_id=recipe.id,
            original_ingredient_id=original_ing.id,
            swap_ingredient_id=swap_ing.id,
        )
    )
    return swap_ing


def _add_instructions(recipe, steps):
    """steps: list of (description, note_text_or_None)"""
    for i, (description, note) in enumerate(steps, start=1):
        instr = Instruction(step=i, description=description, note_text=note)
        db.session.add(instr)
        db.session.flush()
        db.session.add(
            RecipeInstruction(recipe_id=recipe.id, instruction_id=instr.id)
        )


def _add_tags(reg, recipe, names):
    for name in names:
        db.session.add(RecipeTag(recipe_id=recipe.id, tag_id=reg.tag(name).id))


def _add_categories(reg, recipe, names):
    for name in names:
        db.session.add(
            RecipeCategory(recipe_id=recipe.id, category_id=reg.category(name).id)
        )


def _add_appliances(reg, recipe, name_icon_pairs):
    for name, icon in name_icon_pairs:
        db.session.add(
            RecipeAppliance(
                recipe_id=recipe.id, appliance_id=reg.appliance(name, icon).id
            )
        )


def _add_utensils(reg, recipe, name_icon_pairs):
    for name, icon in name_icon_pairs:
        db.session.add(
            RecipeUtensil(
                recipe_id=recipe.id, utensil_id=reg.utensil(name, icon).id
            )
        )


# ---------------------------------------------------------------------------
# Recipe definitions
# ---------------------------------------------------------------------------

def _recipe_liver(reg):
    recipe = Recipe(
        title="Creamy Chicken Liver with Onion, Carrot & Mushroom",
        description="Pan-fried chicken liver in a light cream sauce with "
                     "onion, carrot and mushroom, tossed through pasta.",
        picture="uploads/chicken_liver_cream_pasta.jpg",
        cook_time=25,
        difficulty=Difficulty.MEDIUM,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Chicken Liver", "300", "g", IngredientRole.MAIN)
    pasta = _add_ingredient(reg, recipe, "Pasta", "150", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, pasta, "Potatoes")
    _add_ingredient(reg, recipe, "Onion", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Carrot", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Mushrooms", "150", "g", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Garlic", "1", "clove", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Cream 7%", "200", "ml", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Salt", "1", "tsp", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Black Pepper", "1", "tsp", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Dinner"])
    _add_categories(reg, recipe, ["Offal"])
    _add_appliances(reg, recipe, [("Frying pan", "frying-pan")])
    _add_utensils(reg, recipe, [
        ("Small pot", "small-pot"),
        ("Spatula", "spatula"),
    ])

    _add_instructions(recipe, [
        ("Fill the small pot about halfway with water, add a teaspoon of "
         "salt, and bring it to a boil.", None),
        ("Add the pasta and cook according to the packaging instructions.",
         None),
        ("Meanwhile, chop the onion, carrot and mushrooms (and the garlic, "
         "if using).", "This is a good moment to get everything ready, "
         "since the next steps move quickly."),
        ("Fry the chicken liver on high heat (setting 5) for 5 minutes.",
         None),
        ("Add the onion and carrot (and garlic) and fry for 2 minutes.",
         None),
        ("Add the mushrooms, salt and pepper, and fry for 3 minutes.", None),
        ("Add the cream, reduce the heat to low (setting 3), and let it "
         "cook for 10 minutes.", None),
        ("Just before draining the pasta, scoop out a couple of "
         "tablespoons of the starchy cooking water and stir it into the "
         "sauce.", "This helps the sauce cling to the pasta instead of "
         "sliding off."),
        ("Drain the pasta and add it to the sauce, tossing to coat before "
         "serving.", None),
    ])
    return recipe


def _recipe_soup(reg):
    recipe = Recipe(
        title="Simple Chicken & Vegetable Soup",
        description="A straightforward chicken soup with soup vegetables "
                     "and vermicelli, built on a light bouillon.",
        picture="uploads/chicken_vegetable_soup.jpg",
        cook_time=30,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Chicken Breast", "300", "g", IngredientRole.MAIN)
    _add_ingredient(reg, recipe, "Water", "1", "l", IngredientRole.ESSENTIAL)
    bouillon = _add_ingredient(reg, recipe, "Chicken Bouillon Cubes", "3", "pieces", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, bouillon, "Ramen Soup Base")
    soepgroenten = _add_ingredient(reg, recipe, "Soepgroenten Mix", "300", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, soepgroenten, "Onion")
    _add_swap(reg, recipe, soepgroenten, "Carrot")
    vermicelli = _add_ingredient(reg, recipe, "Vermicelli", "100", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, vermicelli, "Lentils")
    _add_swap(reg, recipe, vermicelli, "Potato")
    _add_ingredient(reg, recipe, "Salt", "1", "tsp", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Black Pepper", "1", "tsp", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Soup", "Dinner"])
    _add_categories(reg, recipe, ["Comfort Food"])
    _add_appliances(reg, recipe, [("Stovetop", "stovetop")])
    _add_utensils(reg, recipe, [
        ("Large pot", "large-pot"),
        ("Ladle", "ladle"),
    ])

    _add_instructions(recipe, [
        ("Dissolve the bouillon cubes in the water in a large pot and "
         "bring to a boil.", "If you're using whole onion and carrot "
         "instead of the soup vegetable mix, this is the time to cut "
         "them."),
        ("Add the chicken and the soup vegetables (or onion and carrot), "
         "and let it simmer for 15 minutes.", None),
        ("Season with salt and pepper to taste.", None),
        ("Add the vermicelli and turn off the heat. Let it sit for a few "
         "minutes until tender.", "Vermicelli cooks fast — adding it off "
         "the heat keeps it from turning mushy."),
        ("Serve hot.", None),
    ])
    return recipe


def _recipe_stew(reg):
    recipe = Recipe(
        title="Beef Stew with Mushrooms",
        description="A slow, simple beef stew with mushroom, onion and "
                     "carrot — worth the wait.",
        picture="uploads/beef_stew_mushroom.jpg",
        cook_time=120,
        difficulty=Difficulty.MEDIUM,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Runderriblap (Stewing Beef)", "550", "g", IngredientRole.MAIN)
    _add_ingredient(reg, recipe, "Mushrooms", "200", "g", IngredientRole.ESSENTIAL)
    ghee = _add_ingredient(reg, recipe, "Ghee", "20", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, ghee, "Butter")
    _add_ingredient(reg, recipe, "Onion", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Carrot", "2", "pieces", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Beef Bouillon Cubes", "2", "pieces", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Water", "300", "ml", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Salt", "1", "tsp", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Black Pepper", "1", "tsp", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Dinner"])
    _add_categories(reg, recipe, ["Comfort Food"])
    _add_appliances(reg, recipe, [("Stovetop", "stovetop")])
    _add_utensils(reg, recipe, [
        ("Large pot", "large-pot"),
        ("Spatula", "spatula"),
    ])

    _add_instructions(recipe, [
        ("Chop the onion, carrot and mushrooms, and cut the beef into "
         "cubes.", None),
        ("Melt the ghee (or butter) in a large pot over medium-high "
         "heat.", None),
        ("Brown the beef cubes on all sides, about 5 minutes.", None),
        ("Add the onion and carrot, and cook for 3 minutes.", None),
        ("Add the mushrooms and cook for another 3 minutes.", None),
        ("Dissolve the bouillon cubes in the water, pour it into the pot, "
         "and season with salt and pepper. Bring to a boil.", None),
        ("Reduce the heat, cover, and let it simmer for around 100 "
         "minutes, stirring occasionally, until the beef is tender.",
         "Runderriblap needs the full time to become tender — an hour "
         "isn't quite enough, so don't rush this part."),
    ])
    return recipe


def _recipe_curry(reg):
    recipe = Recipe(
        title="Easy Chicken Curry with Vegetables",
        description="A basic weeknight curry with chicken thigh, bell "
                     "pepper and light coconut milk, served over rice.",
        picture="uploads/chicken_curry_vegetables.jpg",
        cook_time=30,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    thighs = _add_ingredient(reg, recipe, "Chicken Thighs", "300", "g", IngredientRole.MAIN)
    _add_swap(reg, recipe, thighs, "Chicken Drumsticks")
    _add_ingredient(reg, recipe, "Onion", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Bell Pepper", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Garlic", "2", "cloves", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Curry Powder", "2", "tbsp", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Coconut Milk (Light)", "400", "ml", IngredientRole.ESSENTIAL)
    rice = _add_ingredient(reg, recipe, "Rice", "200", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, rice, "Potato")
    _add_ingredient(reg, recipe, "Vegetable Oil", "1", "tbsp", IngredientRole.ESSENTIAL)

    _add_tags(reg, recipe, ["Dinner"])
    _add_categories(reg, recipe, ["Comfort Food"])
    _add_appliances(reg, recipe, [("Stovetop", "stovetop")])
    _add_utensils(reg, recipe, [
        ("Small pot", "small-pot"),
        ("Spatula", "spatula"),
    ])

    _add_instructions(recipe, [
        ("Cook the rice according to the packaging instructions.", None),
        ("Chop the onion, bell pepper and garlic, and cut the chicken "
         "thighs into bite-sized pieces (drumsticks can be left whole).",
         None),
        ("Heat the oil in a pan, add the onion and garlic, and fry until "
         "fragrant, about 2 minutes.", None),
        ("Add the chicken and cook until browned, about 5 minutes.", None),
        ("Add the bell pepper and curry powder, stir, and cook for 2 "
         "minutes.", None),
        ("Pour in the coconut milk, bring to a simmer, and cook for 10 "
         "minutes, until the chicken is cooked through and the sauce has "
         "thickened slightly.", "If using drumsticks, give this a few "
         "extra minutes and check the meat comes away from the bone "
         "easily."),
        ("Serve over the rice.", None),
    ])
    return recipe


def _recipe_wok(reg):
    recipe = Recipe(
        title="Chicken (or Shrimp) Wok with Rice",
        description="A quick stir-fry with chicken or shrimp, onion and "
                     "soy sauce, over rice or rice noodles.",
        picture="uploads/chicken_shrimp_wok.jpg",
        cook_time=20,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    chicken = _add_ingredient(reg, recipe, "Chicken Breast", "300", "g", IngredientRole.MAIN)
    _add_swap(reg, recipe, chicken, "Shrimp")
    _add_ingredient(reg, recipe, "Onion", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Soy Sauce", "3", "tbsp", IngredientRole.ESSENTIAL)
    rice = _add_ingredient(reg, recipe, "Rice", "150", "g", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, rice, "Rice Noodles")
    _add_ingredient(reg, recipe, "Sunflower Oil", "1", "tbsp", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Bell Pepper", "1", "piece", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Sesame Seeds", "1", "tsp", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Dinner"])
    _add_categories(reg, recipe, ["Asian"])
    _add_appliances(reg, recipe, [("Wok", "wok")])
    _add_utensils(reg, recipe, [
        ("Small pot", "small-pot"),
        ("Spatula", "spatula"),
    ])

    _add_instructions(recipe, [
        ("Cook the rice according to the packaging instructions. If using "
         "rice noodles instead, soak them in hot water for 5-10 minutes "
         "per the packaging, then set aside — they'll go into the wok "
         "directly later.", None),
        ("Cut the chicken (or shrimp) into bite-sized pieces, and chop "
         "the onion (and bell pepper, if using).", None),
        ("Heat the sunflower oil in a wok over high heat.", None),
        ("Add the chicken (or shrimp) and stir-fry for 5 minutes, until "
         "cooked through.", None),
        ("Add the onion (and bell pepper), and stir-fry for 2 minutes.",
         None),
        ("If using rice noodles, add them into the wok now.", None),
        ("Pour in the soy sauce, toss everything to coat, and stir-fry "
         "for another 1-2 minutes.", None),
        ("Serve over the rice, or straight from the wok if using "
         "noodles. Top with sesame seeds, if using.", None),
    ])
    return recipe


def _recipe_potatoes(reg):
    recipe = Recipe(
        title="Grilled-Style Skin-On Potatoes",
        description="A simple side of skin-on potatoes, fried in ghee "
                     "until golden and crisp.",
        picture="uploads/grilled_skin_on_potatoes.jpg",
        cook_time=30,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Potatoes", "300", "g", IngredientRole.MAIN)
    ghee = _add_ingredient(reg, recipe, "Ghee", "2", "tbsp", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, ghee, "Butter")
    _add_ingredient(reg, recipe, "Salt", "1", "tsp", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Carrot", "1", "piece", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Mushrooms", "100", "g", IngredientRole.OPTIONAL)
    _add_ingredient(reg, recipe, "Onion", "1", "piece", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Side Dish"])
    _add_categories(reg, recipe, ["Comfort Food"])
    _add_appliances(reg, recipe, [("Frying pan", "frying-pan")])
    _add_utensils(reg, recipe, [
        ("Small pot", "small-pot"),
        ("Spatula", "spatula"),
    ])

    _add_instructions(recipe, [
        ("Wash the potatoes well, keeping the skin on, and cut into "
         "wedges or halves. Chop the carrot, mushrooms and onion too, if "
         "using.", None),
        ("Boil the potatoes in salted water for 10 minutes, then drain "
         "well.", "A short pre-boil means they'll fry through without "
         "burning the outside."),
        ("Heat the ghee (or butter) in a frying pan over medium-high "
         "heat.", None),
        ("Add the potatoes, cut-side down (and the carrot, mushrooms and "
         "onion, if using), and season with salt.", None),
        ("Fry for 15-20 minutes, turning occasionally, until golden and "
         "crisp on the outside and tender inside.", None),
    ])
    return recipe


def _recipe_hutspot(reg):
    recipe = Recipe(
        title="Hutspot with Sausage",
        description="Classic Dutch mashed potato, carrot and onion, "
                     "served with rookworst or curryworst.",
        picture="uploads/hutspot_sausage.jpg",
        cook_time=25,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Hutspot Mix (Potato, Carrot & Onion)", "500", "g", IngredientRole.MAIN)
    rookworst = _add_ingredient(reg, recipe, "Rookworst", "1", "package", IngredientRole.ESSENTIAL)
    _add_swap(reg, recipe, rookworst, "Curryworst")
    _add_ingredient(reg, recipe, "Butter", "20", "g", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Milk", "50", "ml", IngredientRole.OPTIONAL)

    _add_tags(reg, recipe, ["Dinner"])
    _add_categories(reg, recipe, ["Dutch"])
    _add_appliances(reg, recipe, [
        ("Stovetop", "stovetop"),
        ("Microwave", "microwave"),
        ("Air Fryer", "air-fryer"),
    ])
    _add_utensils(reg, recipe, [
        ("Small pot", "small-pot"),
        ("Potato masher", "potato-masher"),
    ])

    _add_instructions(recipe, [
        ("Boil the hutspot mix in salted water according to the "
         "packaging instructions, about 20 minutes.", None),
        ("Meanwhile, heat the sausage: microwave the rookworst according "
         "to its packaging instructions, or air fry the curryworst for "
         "15 minutes at 170°C.", None),
        ("Drain the cooked vegetables and mash with the butter and a "
         "splash of milk until smooth.", None),
        ("Season with salt and pepper to taste.", None),
        ("Serve the mash with the sliced sausage on top or on the "
         "side.", None),
    ])
    return recipe


def _recipe_salad(reg):
    recipe = Recipe(
        title="Fresh Iceberg Salad",
        description="A crisp, no-cook salad of iceberg lettuce, cherry "
                     "tomato, cucumber and bell pepper.",
        picture="uploads/fresh_iceberg_salad.jpg",
        cook_time=5,
        difficulty=Difficulty.EASY,
    )
    db.session.add(recipe)
    db.session.flush()

    _add_ingredient(reg, recipe, "Iceberg Lettuce", "1/3", "head", IngredientRole.MAIN)
    _add_ingredient(reg, recipe, "Onion", "1/4", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Cherry Tomatoes", "6", "pieces", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Bell Pepper", "1", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "Cucumber", "1/4", "piece", IngredientRole.ESSENTIAL)
    _add_ingredient(reg, recipe, "White Vinegar", "1", "tbsp", IngredientRole.ESSENTIAL)
    mayo = _add_ingredient(reg, recipe, "Mayonnaise", "1", "tbsp", IngredientRole.OPTIONAL)
    _add_swap(reg, recipe, mayo, "Olive Oil")
    _add_swap(reg, recipe, mayo, "Balsamic Vinegar")

    _add_tags(reg, recipe, ["Side Dish", "Salad"])
    _add_categories(reg, recipe, ["Comfort Food"])
    _add_utensils(reg, recipe, [("Peeler", "peeler")])

    _add_instructions(recipe, [
        ("Wash and chop the iceberg lettuce, onion, cherry tomatoes, "
         "bell pepper and cucumber.", None),
        ("Combine everything in a large bowl and toss with the white "
         "vinegar.", None),
        ("Add the mayonnaise and toss to coat (or use olive oil and "
         "balsamic vinegar instead, for a lighter dressing).", None),
        ("Season with salt and pepper to taste, and serve immediately.",
         None),
    ])
    return recipe


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------

@curated_seed_bp.cli.command("run")
def curated_recipes():
    """Seed the 8 curated recipes. Safe to run alongside `flask seed run`."""
    reg = Registry()

    existing_titles = {
        r[0] for r in db.session.execute(db.select(Recipe.title)).all()
    }

    # (title, builder) pairs — title is checked *before* building, so a
    # duplicate is skipped cleanly without touching anything already
    # added earlier in this same run.
    builders = [
        ("Creamy Chicken Liver", _recipe_liver),
        ("Chicken Soup", _recipe_soup),
        ("Beef Stew", _recipe_stew),
        ("Chicken Curry", _recipe_curry),
        ("Wok", _recipe_wok),
        ("Grilled Potatoes", _recipe_potatoes),
        ("Hutspot", _recipe_hutspot),
        ("The BestSalad", _recipe_salad),
    ]

    added = 0
    for title, build in builders:
        if title in existing_titles:
            click.echo(f"Skipped (already exists): {title}")
            continue
        build(reg)
        existing_titles.add(title)
        added += 1

    db.session.commit()
    click.echo(f"Seeded {added} curated recipes.")