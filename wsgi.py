from app import create_app
from app.config import DevelopmentConfig

app = create_app(DevelopmentConfig) # using development config for now

if __name__ == "__main__":
    app.run(debug=True)