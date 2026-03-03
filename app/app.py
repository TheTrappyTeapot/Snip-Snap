from pathlib import Path
import os

from flask import Flask
from dotenv import load_dotenv

from .routes import register_routes


def create_app():
    project_root = Path(__file__).resolve().parent.parent  # .../Snip-Snap
    load_dotenv(project_root / ".env")  # .../Snip-Snap/.env

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret")

    register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)