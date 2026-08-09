from flask import Blueprint, render_template

from ...extensions import db
from ...models import Recipe

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    items = db.session.execute(
        db.select(Recipe).order_by(Recipe.created_at.desc())
    ).scalars().all()
    return render_template("main/index.html", items=items)