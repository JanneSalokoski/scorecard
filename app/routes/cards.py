from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from app.db import get_db

import hashlib
import time


def create_slug(data: str) -> str:
    salt = str(time.time_ns())
    salted_string = f"{data}-{salt}"
    return hashlib.sha256(salted_string.encode()).hexdigest()[:12]


bp = Blueprint("cards", __name__)


@bp.route("/", methods=["GET", "POST"])
def create_card():
    if request.method == "GET":
        return render_template("create_card.html")

    card_name = request.form.get("card_name", "").strip()

    if card_name == "":
        flash("Error: Card name must be provided")
        return redirect(url_for("index.index"))

    slug = create_slug(card_name)

    db = get_db()

    query = "INSERT INTO cards (slug, card_name) VALUES (?, ?)"
    values = (slug, card_name)

    if "user_id" in session:
        query = "INSERT INTO cards (slug, card_name, user_id) VALUES (?, ?, ?)"
        values = (slug, card_name, session["user_id"])

    try:
        db.execute(query, values)
        db.commit()
    except Exception as e:
        flash(f"Error: {e}")
        return redirect(url_for("index.index"))

    return redirect(url_for("cards.view_card", slug=slug))


@bp.route("/<string:slug>")
def view_card(slug: str):
    return slug
