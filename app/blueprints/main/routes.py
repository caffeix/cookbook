from flask import Blueprint, render_template

from ...extensions import db
from ...models import Recipe

main_bp = Blueprint("main", __name__)

# main_bp index route replaced by recipes_bp list_recipes on '/'