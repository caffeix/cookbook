from flask import Blueprint, render_template, request
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...models import Recipe, Category
from ...models.recipe_tag import RecipeTag
from ...models.recipe_category import RecipeCategory
from ...models.recipe_appliance import RecipeAppliance
from ...models.recipe_utensil import RecipeUtensil

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/", strict_slashes=False)
def list_recipes():
    """GET /recipes — recipe list with optional single-category filter."""
    selected_slug = (request.args.get("category", "") or "").strip().lower() or None

    # Base query: most recent first, with all card-rendering relationships pre-loaded
    # selectinload fires separate IN queries — no N+1 and no join conflicts
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

    # Filter by category slug using a correlated subquery so the selectinload
    # relationships above are still loaded correctly (a direct JOIN on the same
    # relationship would cause a conflict with selectinload)
    if selected_slug:
        matching_ids = (
            db.select(RecipeCategory.recipe_id)
            .join(RecipeCategory.category)
            .where(Category.slug == selected_slug)
            .scalar_subquery()
        )
        stmt = stmt.where(Recipe.id.in_(matching_ids))

    recipes = db.session.execute(stmt).scalars().all()

    # All categories for the chip bar, ordered alphabetically
    categories = (
        db.session.execute(db.select(Category).order_by(Category.name))
        .scalars()
        .all()
    )

    return render_template(
        "recipes/list.html",
        recipes=recipes,
        categories=categories,
        selected_category=selected_slug,
    )
