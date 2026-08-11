import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import Recipe, Category, RecipeCategory
from app.utils import slugify


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_recipe_card_category_badge(app, client):
    with app.app_context():
        cat = Category(name="Italian", slug=slugify("Italian"), icon="🍝")
        recipe = Recipe(title="Pesto Pasta", description="Delicious pesto")
        db.session.add_all([cat, recipe])
        db.session.flush()

        db.session.add(RecipeCategory(recipe_id=recipe.id, category_id=cat.id))
        db.session.commit()

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'class="recipe-card__category-badge"' in html
    assert "Italian" in html
    assert "🍝" in html
