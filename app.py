import sqlite3
from pathlib import Path

from flask import Flask, render_template, request


app = Flask(__name__)


def get_db_connection():
    database_path = Path(app.instance_path) / "prompts.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    title = ""
    prompt_text = ""
    submitted = False
    saved = False

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        prompt_text = request.form.get("prompt", "").strip()
        submitted = bool(title and prompt_text)

        if submitted and request.form.get("save_prompt") == "yes":
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO prompts (title, prompt) VALUES (?, ?)",
                    (title, prompt_text),
                )
            saved = True

    return render_template(
        "prompt.html",
        title=title,
        prompt_text=prompt_text,
        submitted=submitted,
        saved=saved,
    )


@app.route("/landscape", methods=["GET", "POST"])
def landscape():
    description = ""
    time_of_day = "sunrise"
    weather = "clear"
    season = "spring"

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        time_of_day = request.form.get("time_of_day", "sunrise")
        weather = request.form.get("weather", "clear")
        season = request.form.get("season", "spring")

    return render_template(
        "landscape.html",
        description=description,
        time_of_day=time_of_day,
        weather=weather,
        season=season,
    )


if __name__ == "__main__":
    app.run(debug=True)
