from flask import Flask

app = Flask(__name__)


def create_app():
    app = Flask(__name__)

    from .routes import register_blueprints

    register_blueprints(app)

    return app
