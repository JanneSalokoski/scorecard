from flask import Blueprint, redirect, request, session, url_for

bp = Blueprint("theme", __name__)


@bp.route("/set", methods=["POST"])
def set_theme():
    theme = request.form.get("theme")
    if theme in ["light", "dark"]:
        session["theme"] = theme

        return redirect(request.referrer or url_for("index.index"))
