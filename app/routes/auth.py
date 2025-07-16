import sqlite3

from flask import Blueprint, render_template, redirect, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password_1 = request.form.get("password-1", "")
    password_2 = request.form.get("password-2", "")

    error = None

    if not username:
        error = "Username is required"
    elif not password_1:
        error = "Password is required"
    elif password_1 != password_2:
        error = "Passwords do not match"

    if error:
        flash(error)
        return render_template("register.html", username=username)

    db = get_db()
    password_hash = generate_password_hash(password_1)

    try:
        query = "INSERT INTO users (username, hash) VALUES (?, ?)"
        db.execute(query, (username, password_hash))
        db.commit()
    except sqlite3.IntegrityError:
        flash("Error: username is taken")
        return render_template("register.html", username=username)

    return redirect("/auth/login")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    error = None

    if not username:
        error = "Username is required"
    elif not password:
        error = "Password is required"

    if error:
        flash(error)
        return render_template("login.html", username=username)

    db = get_db()

    try:
        query = "SELECT id, username, hash FROM users WHERE username = ?"
        row = db.execute(query, (username,)).fetchone()

        if row is None:
            error = "Username not found"
        elif not check_password_hash(row["hash"], password):
            error = "Incorrect password"

        if error:
            flash(error)
            return render_template("login.html", username=username)

        session["user_id"] = row["id"]

    except Exception as e:
        flash(f"Error: {e}")
        return render_template("login.html", username=username)

    return redirect("/auth/login")


@bp.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")
