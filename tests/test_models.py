"""Phase 1 tests: verify modern SQLAlchemy models and slug generation."""
import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import (
    Recipe, Category, Tag, Ingredient,
    RecipeTag, RecipeCategory, RecipeIngredient,
    Replaceable,
)
from app.models.recipe_tag import RecipeTag
from app.models.recipe_category import RecipeCategory
from app.utils import slugify
from sqlalchemy.orm import selectinload


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def seeded_app(app):
    """Create a minimal dataset for testing relationships."""
    cat = Category(name="Italian", slug=slugify("Italian"))
    tag1 = Tag(name="Italian", slug=slugify("Italian"))
    tag2 = Tag(name="Quick Meals", slug=slugify("Quick Meals"))
    ingr = Ingredient(name="Olive Oil", slug=slugify("Olive Oil"))
    recipe = Recipe(
        title="Garlic Pasta",
        description="Simple weeknight pasta",
        cook_time=20,
        difficulty="easy",
    )
    db.session.add_all([cat, tag1, tag2, ingr, recipe])
    db.session.flush()

    db.session.add_all([
        RecipeCategory(recipe_id=recipe.id, category_id=cat.id),
        RecipeTag(recipe_id=recipe.id, tag_id=tag1.id),
        RecipeTag(recipe_id=recipe.id, tag_id=tag2.id),
        RecipeIngredient(recipe_id=recipe.id, ingredient_id=ingr.id, quantity="2", unit="tbsp"),
    ])
    db.session.commit()
    return app


# ── slugify() utility ─────────────────────────────────────────────────────────

def test_slugify_single_word():
    assert slugify("Italian") == "italian"


def test_slugify_two_words():
    assert slugify("Quick Meals") == "quick-meals"


def test_slugify_accents():
    assert slugify("Crème Brûlée") == "creme-brulee"


def test_slugify_punctuation():
    assert slugify("Salt & Pepper") == "salt-pepper"


# ── Model column types (Mapped / mapped_column) ───────────────────────────────

def test_recipe_fields(seeded_app):
    recipe = db.session.execute(db.select(Recipe)).scalars().first()
    assert recipe.title == "Garlic Pasta"
    assert recipe.cook_time == 20
    assert recipe.difficulty == "easy"
    assert recipe.picture is None


def test_category_has_slug(seeded_app):
    cat = db.session.execute(db.select(Category)).scalars().first()
    assert cat.name == "Italian"
    assert cat.slug == "italian"


def test_tag_has_slug(seeded_app):
    tags = db.session.execute(db.select(Tag)).scalars().all()
    slugs = {t.slug for t in tags}
    assert "italian" in slugs
    assert "quick-meals" in slugs


def test_ingredient_has_slug(seeded_app):
    ingr = db.session.execute(db.select(Ingredient)).scalars().first()
    assert ingr.slug == "olive-oil"


# ── Association proxies ───────────────────────────────────────────────────────

def test_recipe_tags_via_proxy(seeded_app):
    recipe = db.session.execute(
        db.select(Recipe)
        .options(selectinload(Recipe.tag_links).selectinload(RecipeTag.tag))
    ).scalars().first()
    tag_names = [t.name for t in recipe.tags]
    assert "Italian" in tag_names
    assert "Quick Meals" in tag_names


def test_recipe_categories_via_proxy(seeded_app):
    recipe = db.session.execute(
        db.select(Recipe)
        .options(selectinload(Recipe.category_links).selectinload(RecipeCategory.category))
    ).scalars().first()
    cat_names = [c.name for c in recipe.categories]
    assert "Italian" in cat_names


def test_recipe_ingredients_via_proxy(seeded_app):
    recipe = db.session.execute(
        db.select(Recipe)
        .options(selectinload(Recipe.ingredient_links))
    ).scalars().first()
    assert len(recipe.ingredient_links) == 1
    assert recipe.ingredient_links[0].quantity == "2"
    assert recipe.ingredient_links[0].unit == "tbsp"


# ── Replaceable (two FK disambiguation) ──────────────────────────────────────

def test_replaceable_two_fk(seeded_app):
    spaghetti = Ingredient(name="Spaghetti", slug=slugify("Spaghetti"))
    fusilli = Ingredient(name="Fusilli", slug=slugify("Fusilli"))
    recipe = db.session.execute(db.select(Recipe)).scalars().first()
    db.session.add_all([spaghetti, fusilli])
    db.session.flush()

    rep = Replaceable(
        recipe_id=recipe.id,
        original_ingredient_id=spaghetti.id,
        swap_ingredient_id=fusilli.id,
    )
    db.session.add(rep)
    db.session.commit()

    loaded = db.session.execute(db.select(Replaceable)).scalars().first()
    assert loaded.original_ingredient.name == "Spaghetti"
    assert loaded.swap_ingredient.name == "Fusilli"


# ── Timestamps ───────────────────────────────────────────────────────────────

def test_timestamps_populated(seeded_app):
    recipe = db.session.execute(db.select(Recipe)).scalars().first()
    assert recipe.created_at is not None
    assert recipe.updated_at is not None
