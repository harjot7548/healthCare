from flask import Flask
from .routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    app.register_blueprint(main)

    return app
