from .index import bp as index_bp
from .users import bp as users_bp
from .auth import bp as auth_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
