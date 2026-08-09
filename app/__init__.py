from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from .extensions import db, migrate
from .seed import seed_bp
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.main.routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(seed_bp)

    from . import models

    @app.route("/")
    def index():
        return "Hello World"

    return app