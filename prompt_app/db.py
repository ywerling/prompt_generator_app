import sqlite3
from pathlib import Path

from flask import current_app, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def get_db():
    if "db" not in g:
        database_path = Path(current_app.instance_path) / "prompts.db"
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute(SCHEMA)
    return g.db


def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def save_prompt(title, prompt):
    connection = get_db()
    connection.execute("INSERT INTO prompts (title, prompt) VALUES (?, ?)", (title, prompt))
    connection.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
