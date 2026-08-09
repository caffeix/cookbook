import pytest
from app import create_app
from app.extensions import db
from app.config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200