from flask import Blueprint, render_template
from app.db import get_db

bp = Blueprint("users", __name__)


@bp.route("/users")
def users():
    db = get_db()
    users = db.execute("SELECT id, username FROM users").fetchall()
    return render_template("users.html", users=users)
