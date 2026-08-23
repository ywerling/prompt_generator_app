from flask import Blueprint, render_template, request

from ..db import save_prompt

prompts_bp = Blueprint("prompts", __name__)


@prompts_bp.route("/prompt", methods=["GET", "POST"])
def workspace():
    title = prompt_text = ""
    submitted = saved = False
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        prompt_text = request.form.get("prompt", "").strip()
        submitted = bool(title and prompt_text)
        if submitted and request.form.get("save_prompt") == "yes":
            save_prompt(title, prompt_text)
            saved = True
    return render_template("prompt.html", title=title, prompt_text=prompt_text, submitted=submitted, saved=saved)
