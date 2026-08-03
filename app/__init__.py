from flask import Flask
from dotenv import load_dotenv

from .config import Config

def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.route("/")
    def index():
        return "Hello World"

    return app