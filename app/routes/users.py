from flask import Blueprint, render_template, flash, session, redirect, url_for
from app.db import get_db

bp = Blueprint("users", __name__)


@bp.route("/users")
def users():
    db = get_db()
    users = db.execute("SELECT id, username FROM users").fetchall()
    return render_template("users.html", users=users)


@bp.route("/users/<int:user_id>")
def view_user(user_id: int):
    # To-do: admin can view any user

    if "user_id" not in session:
        flash("You have to be logged in")
        return redirect(url_for("auth.login"))

    elif user_id != session["user_id"]:
        flash("Access denied")
        return redirect(url_for("index.index"))

    db = get_db()

    error = None

    try:
        user = db.execute(
            "SELECT id, username FROM users WHERE id=?", (user_id,)
        ).fetchone()

        if not user:
            error = "User not found"

    except Exception as e:
        error = f"Error: {e}"

    if error:
        flash(error)
        return render_template("view_user.html", user=None, user_id=user_id)

    return render_template("view_user.html", user=user, user_id=user_id)


@bp.route("/users/me")
def view_me():
    if "user_id" not in session:
        flash("You have to be logged in")
        return redirect(url_for("auth.login"))

    return redirect(url_for("users.view_user", user_id=session["user_id"]))
