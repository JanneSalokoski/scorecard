from .index import bp as index_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
