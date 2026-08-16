import sqlite3
from pathlib import Path

from flask import Flask, render_template, request


app = Flask(__name__)


LANDSCAPE_DROPDOWNS = [
    {
        "name": "time_of_day",
        "label": "Time of day",
        "options": ["sunrise", "morning", "midday", "afternoon", "evening", "sunset", "night"],
        "default": "sunrise",
    },
    {
        "name": "weather",
        "label": "Weather",
        "options": ["clear", "cloudy", "misty", "rainy", "stormy", "snowy"],
        "default": "clear",
    },
    {
        "name": "season",
        "label": "Season",
        "options": ["spring", "summer", "autumn", "winter"],
        "default": "spring",
    },
]


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
    generated_prompt = ""
    selections = {
        dropdown["name"]: dropdown["default"]
        for dropdown in LANDSCAPE_DROPDOWNS
    }

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        for dropdown in LANDSCAPE_DROPDOWNS:
            selected = request.form.get(dropdown["name"], dropdown["default"])
            if selected in dropdown["options"]:
                selections[dropdown["name"]] = selected
        generated_prompt = request.form.get("generated_prompt", "").strip()

        if request.form.get("action") == "generate" and description:
            generated_prompt = (
                f"{description} Set during {selections['time_of_day']}, with "
                f"{selections['weather']} weather in {selections['season']}. "
                "Expansive landscape composition, rich natural detail, "
                "atmospheric depth, and cinematic lighting."
            )

    return render_template(
        "landscape.html",
        description=description,
        dropdowns=LANDSCAPE_DROPDOWNS,
        selections=selections,
        generated_prompt=generated_prompt,
    )


if __name__ == "__main__":
    app.run(debug=True)
