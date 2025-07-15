import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "scorecard.sqlite"),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import register_blueprints

    register_blueprints(app)

    from . import db

    app.teardown_appcontext(db.close_db)
    db.register_cli(app)

    return app
