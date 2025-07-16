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


@bp.route("/<string:slug>", methods=["GET", "POST"])
def view_card(slug: str):
    if request.method == "GET":
        db = get_db()

        card_query = """
        SELECT
            cards.id AS card_id,
            cards.slug as card_slug,
            cards.card_name,
            cards.created_at AS card_created,
            scores.id AS score_id,
            scores.player_name AS player_name,
            scores.points AS points,
            scores.created_at AS score_created
        FROM
            cards
        LEFT JOIN
            scores
        ON
            cards.id = scores.card_id
        WHERE cards.slug = ?;
        """

        card_rows = db.execute(card_query, (slug,)).fetchall()

        if not card_rows:
            flash("Error: card not found")
            return redirect(url_for("index.index"))

        card = {
            "id": card_rows[0]["card_id"],
            "slug": card_rows[0]["card_slug"],
            "card_name": card_rows[0]["card_name"],
            "created_at": card_rows[0]["card_created"],
        }

        scores = [
            {
                "id": row["score_id"],
                "player_name": row["player_name"],
                "points": row["points"],
                "created_at": row["score_created"],
            }
            for row in card_rows
            if row["score_id"] is not None
        ]

        return render_template("view_card.html", card=card, scores=scores)

    return "Not supported!"
