import os

class Config:
    """Base config — shared defaults."""
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-only-insecure-key")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False