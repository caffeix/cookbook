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


def test_recipe_search_filtering(app, client):
    with app.app_context():
        recipe1 = Recipe(title="Spaghetti Carbonara", description="Classic Italian pasta dish")
        recipe2 = Recipe(title="Avocado Toast", description="Quick breakfast toast")
        db.session.add_all([recipe1, recipe2])
        db.session.commit()

    # Search for "carbonara"
    res1 = client.get("/?q=carbonara")
    assert res1.status_code == 200
    html1 = res1.get_data(as_text=True)
    assert "Spaghetti Carbonara" in html1
    assert "Avocado Toast" not in html1

    # Search for "breakfast" (in description)
    res2 = client.get("/?q=breakfast")
    assert res2.status_code == 200
    html2 = res2.get_data(as_text=True)
    assert "Avocado Toast" in html2
    assert "Spaghetti Carbonara" not in html2

    # Search with no match
    res3 = client.get("/?q=nonexistentkeyword")
    assert res3.status_code == 200
    html3 = res3.get_data(as_text=True)
    assert 'No recipes found matching "nonexistentkeyword"' in html3
    assert "Spaghetti Carbonara" not in html3
    assert "Avocado Toast" not in html3


def test_recipe_search_appliances_utensils_instructions(app, client):
    from app.models import Appliance, RecipeAppliance, Instruction, RecipeInstruction
    with app.app_context():
        appl = Appliance(name="Air Fryer")
        inst = Instruction(step=1, description="Air fry at 200 degrees")
        recipe = Recipe(title="Crispy Fries", description="Golden fries")
        db.session.add_all([appl, inst, recipe])
        db.session.flush()

        db.session.add(RecipeAppliance(recipe_id=recipe.id, appliance_id=appl.id))
        db.session.add(RecipeInstruction(recipe_id=recipe.id, instruction_id=inst.id))
        db.session.commit()

    # Search for "air fryer"
    res1 = client.get("/?q=air+fryer")
    assert res1.status_code == 200
    assert "Crispy Fries" in res1.get_data(as_text=True)

    # Search for instruction step text "200 degrees"
    res2 = client.get("/?q=200+degrees")
    assert res2.status_code == 200
    assert "Crispy Fries" in res2.get_data(as_text=True)


def test_ingredient_quantity_column(app, client):
    from app.models import Ingredient, RecipeIngredient, IngredientRole
    with app.app_context():
        ing1 = Ingredient(name="Garlic", slug=slugify("Garlic"))
        ing2 = Ingredient(name="Parsley", slug=slugify("Parsley"))
        recipe = Recipe(title="Garlic Parsley Salad", description="Fresh salad")
        db.session.add_all([ing1, ing2, recipe])
        db.session.flush()

        db.session.add_all([
            RecipeIngredient(recipe_id=recipe.id, ingredient_id=ing1.id, quantity="2", unit="cloves", role=IngredientRole.MAIN),
            RecipeIngredient(recipe_id=recipe.id, ingredient_id=ing2.id, quantity=None, unit=None, role=IngredientRole.OPTIONAL),
        ])
        db.session.commit()
        recipe_id = recipe.id

    res = client.get(f"/recipes/{recipe_id}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    assert '<span class="detail-ingredient__qty">2 cloves</span>' in html
    assert '<span class="detail-ingredient__qty"></span>' in html



