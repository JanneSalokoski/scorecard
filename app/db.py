import sqlite3
import click
import os

from flask import g, current_app
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        db_path = os.path.join(current_app.instance_path, "scorecard.sqlite")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear and initialize the database"""
    init_db()
    click.echo("Initialized database")


def register_cli(app):
    app.cli.add_command(init_db_command)
