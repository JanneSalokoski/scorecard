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
    db = get_db()

    if request.method == "GET":
        card_query = """
        SELECT
            cards.id AS card_id,
            cards.slug as card_slug,
            cards.card_name,
            cards.created_at AS card_created,
            scores.id AS score_id,
            scores.player_name AS player_name,
            scores.points AS points,
            scores.round_number,
            scores.created_at AS score_created
        FROM
            cards
        LEFT JOIN
            scores
        ON
            cards.id = scores.card_id
        WHERE cards.slug = ?
        ORDER BY scores.round_number, scores.player_name
        ;
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

        from collections import defaultdict

        round_scores = defaultdict(dict)
        player_names = set()

        for row in card_rows:
            if row["score_id"] is not None:
                player = row["player_name"]
                round_num = row["round_number"]
                round_scores[round_num][player] = row["points"]
                player_names.add(player)

        player_names = sorted(player_names)
        round_scores = dict(sorted(round_scores.items()))

        return render_template(
            "view_card.html", card=card, players=player_names, scores=round_scores
        )

    card_id_query = "SELECT id FROM cards WHERE cards.slug = ?"
    card_id = db.execute(card_id_query, (slug,)).fetchone()["id"]

    if not card_id:
        flash("Error: card not found")
        return redirect(url_for("index.index"))

    player_name = request.form.get("player_name")
    if not player_name:
        flash("Error: no player given")
        return redirect(url_for("cards.view_card", slug=slug))

    points = request.form.get("points")
    if not points:
        flash("Error: no points given")
        return redirect(url_for("cards.view_card", slug=slug))

    round_number = request.form.get("round_number")
    if not round_number:
        flash("Error: no round given")
        return redirect(url_for("cards.view_card", slug=slug))

    score_insert_query = "INSERT INTO scores (card_id, player_name, points, round_number) VALUES (?, ?, ?, ?)"

    try:
        db.execute(score_insert_query, (card_id, player_name, points, round_number))
        db.commit()
    except Exception as e:
        flash(f"Error: {e}")
        return redirect(url_for("index.index"))

    return redirect(url_for("cards.view_card", slug=slug))
