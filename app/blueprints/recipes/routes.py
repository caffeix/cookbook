from flask import Blueprint, abort, render_template, request
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...models import Recipe, Category, Difficulty
from ...models.tag import Tag
from ...models.appliance import Appliance
from ...models.utensil import Utensil
from ...models.ingredient import Ingredient
from ...models.instruction import Instruction
from ...models.recipe_tag import RecipeTag
from ...models.recipe_category import RecipeCategory
from ...models.recipe_appliance import RecipeAppliance
from ...models.recipe_utensil import RecipeUtensil
from ...models.recipe_ingredient import RecipeIngredient
from ...models.recipe_instruction import RecipeInstruction
from ...models.replaceable import Replaceable

recipes_bp = Blueprint("recipes", __name__)


def _parse_slugs(param_name: str) -> list[str]:
    """Parse comma-separated slug list from query params; return [] if absent."""
    raw = (request.args.get(param_name, "") or "").strip()
    return [s.strip().lower() for s in raw.split(",") if s.strip()] if raw else []


def _parse_ids(param_name: str) -> list[int]:
    """Parse comma-separated integer id list from query params; return [] if absent."""
    raw = (request.args.get(param_name, "") or "").strip()
    ids = []
    for s in raw.split(","):
        s = s.strip()
        if s.isdigit():
            ids.append(int(s))
    return ids


@recipes_bp.route("/", strict_slashes=False)
def list_recipes():
    """GET / — recipe list with multi-facet filtering.

    Filter params (all optional, AND logic between facets):
      ?q=search_term       — search query in title, description, tags, ingredients, categories, appliances, utensils, instructions
      ?category=slug       — single category slug
      ?difficulty=easy     — easy | medium | hard
      ?time_max=20         — cook_time <= N minutes
      ?tags=slug1,slug2    — OR within selected tags
      ?appliances=1,2      — appliance IDs (OR within set)
      ?utensils=3,4        — utensil IDs (OR within set)
      ?ingredients=slug1   — ingredient slugs (OR within set)
    """
    search_query = (request.args.get("q", "") or "").strip()
    selected_category = (request.args.get("category", "") or "").strip().lower() or None
    selected_difficulty = (request.args.get("difficulty", "") or "").strip().lower() or None

    time_max_raw = (request.args.get("time_max", "") or "").strip()
    selected_time_max = int(time_max_raw) if time_max_raw.isdigit() else None

    selected_tags = _parse_slugs("tags")
    selected_appliances = _parse_ids("appliances")
    selected_utensils = _parse_ids("utensils")
    selected_ingredients = _parse_slugs("ingredients")

    # Base query — selectinload avoids N+1 without conflicting with WHERE subqueries
    stmt = (
        db.select(Recipe)
        .options(
            selectinload(Recipe.tag_links).selectinload(RecipeTag.tag),
            selectinload(Recipe.category_links).selectinload(RecipeCategory.category),
            selectinload(Recipe.appliance_links).selectinload(RecipeAppliance.appliance),
            selectinload(Recipe.utensil_links).selectinload(RecipeUtensil.utensil),
        )
        .order_by(Recipe.created_at.desc())
    )

    # ── Apply filters (AND between facets) ──────────────────────────────────

    if search_query:
        pattern = f"%{search_query}%"
        ingr_match_ids = (
            db.select(RecipeIngredient.recipe_id)
            .join(RecipeIngredient.ingredient)
            .where(Ingredient.name.ilike(pattern))
            .scalar_subquery()
        )
        tag_match_ids = (
            db.select(RecipeTag.recipe_id)
            .join(RecipeTag.tag)
            .where(Tag.name.ilike(pattern))
            .scalar_subquery()
        )
        cat_match_ids = (
            db.select(RecipeCategory.recipe_id)
            .join(RecipeCategory.category)
            .where(Category.name.ilike(pattern))
            .scalar_subquery()
        )
        appl_match_ids = (
            db.select(RecipeAppliance.recipe_id)
            .join(RecipeAppliance.appliance)
            .where(Appliance.name.ilike(pattern))
            .scalar_subquery()
        )
        uten_match_ids = (
            db.select(RecipeUtensil.recipe_id)
            .join(RecipeUtensil.utensil)
            .where(Utensil.name.ilike(pattern))
            .scalar_subquery()
        )
        inst_match_ids = (
            db.select(RecipeInstruction.recipe_id)
            .join(RecipeInstruction.instruction)
            .where(
                or_(
                    Instruction.description.ilike(pattern),
                    Instruction.note_text.ilike(pattern),
                )
            )
            .scalar_subquery()
        )
        stmt = stmt.where(
            or_(
                Recipe.title.ilike(pattern),
                Recipe.description.ilike(pattern),
                Recipe.id.in_(ingr_match_ids),
                Recipe.id.in_(tag_match_ids),
                Recipe.id.in_(cat_match_ids),
                Recipe.id.in_(appl_match_ids),
                Recipe.id.in_(uten_match_ids),
                Recipe.id.in_(inst_match_ids),
            )
        )

    if selected_category:
        cat_ids = (
            db.select(RecipeCategory.recipe_id)
            .join(RecipeCategory.category)
            .where(Category.slug == selected_category)
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(cat_ids))

    if selected_difficulty:
        # Map the raw string to the Difficulty enum value for a type-safe comparison
        difficulty_enum = Difficulty(selected_difficulty) if selected_difficulty in Difficulty._value2member_map_ else None
        if difficulty_enum:
            stmt = stmt.where(Recipe.difficulty == difficulty_enum)

    if selected_time_max:
        stmt = stmt.where(Recipe.cook_time <= selected_time_max)

    if selected_tags:
        # OR within tags: recipe matches if it has ANY of the selected tag slugs
        tag_ids = (
            db.select(RecipeTag.recipe_id)
            .join(RecipeTag.tag)
            .where(Tag.slug.in_(selected_tags))
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(tag_ids))

    if selected_appliances:
        appl_ids = (
            db.select(RecipeAppliance.recipe_id)
            .where(RecipeAppliance.appliance_id.in_(selected_appliances))
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(appl_ids))

    if selected_utensils:
        uten_ids = (
            db.select(RecipeUtensil.recipe_id)
            .where(RecipeUtensil.utensil_id.in_(selected_utensils))
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(uten_ids))

    if selected_ingredients:
        ingr_ids = (
            db.select(RecipeIngredient.recipe_id)
            .join(RecipeIngredient.ingredient)
            .where(Ingredient.slug.in_(selected_ingredients))
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(ingr_ids))

    recipes = db.session.execute(stmt).scalars().all()

    # ── Facet option lists for drawer ───────────────────────────────────────
    categories = (
        db.session.execute(db.select(Category).order_by(Category.name)).scalars().all()
    )
    tags = (
        db.session.execute(db.select(Tag).order_by(Tag.name)).scalars().all()
    )
    appliances_list = (
        db.session.execute(db.select(Appliance).order_by(Appliance.name)).scalars().all()
    )
    utensils_list = (
        db.session.execute(db.select(Utensil).order_by(Utensil.name)).scalars().all()
    )
    ingredients_list = (
        db.session.execute(db.select(Ingredient).order_by(Ingredient.name)).scalars().all()
    )

    # Badge count: number of individual selections across all facets
    active_filter_count = sum([
        1 if selected_category else 0,
        1 if selected_difficulty else 0,
        1 if selected_time_max else 0,
        len(selected_tags),
        len(selected_appliances),
        len(selected_utensils),
        len(selected_ingredients),
    ])

    return render_template(
        "recipes/list.html",
        recipes=recipes,
        categories=categories,
        selected_category=selected_category,
        tags=tags,
        selected_tags=selected_tags,
        appliances_list=appliances_list,
        selected_appliances=[str(i) for i in selected_appliances],
        utensils_list=utensils_list,
        selected_utensils=[str(i) for i in selected_utensils],
        ingredients_list=ingredients_list,
        selected_ingredients=selected_ingredients,
        selected_difficulty=selected_difficulty,
        selected_time_max=selected_time_max,
        active_filter_count=active_filter_count,
    )


@recipes_bp.route("/recipes/<int:id>", strict_slashes=False)
def recipe_detail(id: int):
    """GET /recipes/<id> — recipe detail page.

    Single eager-loaded query covers all relationships, avoiding N+1.
    swap_map gives O(1) substitution lookup in the template.
    """
    stmt = (
        db.select(Recipe)
        .options(
            selectinload(Recipe.ingredient_links).selectinload(RecipeIngredient.ingredient),
            selectinload(Recipe.category_links).selectinload(RecipeCategory.category),
            selectinload(Recipe.tag_links).selectinload(RecipeTag.tag),
            selectinload(Recipe.appliance_links).selectinload(RecipeAppliance.appliance),
            selectinload(Recipe.utensil_links).selectinload(RecipeUtensil.utensil),
            selectinload(Recipe.replaceables).selectinload(Replaceable.original_ingredient),
            selectinload(Recipe.replaceables).selectinload(Replaceable.swap_ingredient),
        )
        .where(Recipe.id == id)
    )
    recipe = db.session.execute(stmt).scalar_one_or_none()
    if recipe is None:
        abort(404)

    # Build swap_map: {original_ingredient_id: swap_ingredient_name}
    swap_map: dict[int, str] = {
        r.original_ingredient_id: r.swap_ingredient.name
        for r in recipe.replaceables
    }

    # Sort instruction_links by step number (nulls sorted last)
    sorted_instruction_links = sorted(
        recipe.instruction_links,
        key=lambda link: (link.instruction.step is None, link.instruction.step or 0),
    )

    return render_template(
        "recipes/detail.html",
        recipe=recipe,
        swap_map=swap_map,
        sorted_instruction_links=sorted_instruction_links,
    )
