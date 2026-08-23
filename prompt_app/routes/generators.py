from flask import Blueprint, render_template, request

from forms import CharacterForm, GenericForm
from utils import process_character_form_data
from ..services.landscape_builder import (
    LANDSCAPE_DROPDOWNS,
    build_landscape_prompt,
    default_selections,
    validated_selections,
)
from ..services.prompt_builder import build_prompt
from ..services.generic_builder import build_generic_prompt
from ..services.template_builder import build_template_prompt, parse_template
from ..db import save_prompt

generators_bp = Blueprint("generators", __name__)


DEFAULT_TEMPLATE = "draw a {PERSON} in the style of {ARTIST}"


@generators_bp.route("/template", methods=["GET", "POST"])
def template_generator():
    template = request.form.get("template", DEFAULT_TEMPLATE).strip() or DEFAULT_TEMPLATE
    segments, placeholders = parse_template(template)
    values = {name: request.form.get(f"value_{name}", "").strip() for name in placeholders}
    generated_prompt = request.form.get("generated_prompt", "").strip()
    action = request.form.get("action")
    saved = False
    error = ""

    if request.method == "POST" and not placeholders:
        error = "Add at least one placeholder such as {PERSON} to the template."
    elif action == "generate":
        missing = [name for name in placeholders if not values[name]]
        if missing:
            error = "Complete every template field before generating the prompt."
        else:
            generated_prompt = build_template_prompt(template, values)
    elif action == "save":
        if generated_prompt:
            save_prompt(f"Template prompt: {generated_prompt[:80]}", generated_prompt)
            saved = True
        else:
            error = "Generate a prompt before saving it."

    return render_template(
        "template_generator.html",
        template=template,
        segments=segments,
        placeholders=placeholders,
        values=values,
        generated_prompt=generated_prompt,
        saved=saved,
        error=error,
    )


@generators_bp.route("/generic", methods=["GET", "POST"])
def generic():
    form = GenericForm()
    result = build_generic_prompt(request.form) if form.validate_on_submit() else None
    return render_template("generic.html", form=form, result=result)


@generators_bp.route("/landscape", methods=["GET", "POST"])
def landscape():
    description = generated_prompt = ""
    selections = default_selections()
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        selections = validated_selections(request.form)
        generated_prompt = request.form.get("generated_prompt", "").strip()
        if request.form.get("action") == "generate" and description:
            generated_prompt = build_landscape_prompt(description, selections)
    return render_template(
        "landscape.html",
        description=description,
        dropdowns=LANDSCAPE_DROPDOWNS,
        selections=selections,
        generated_prompt=generated_prompt,
    )


@generators_bp.route("/prompt_generator", methods=["GET", "POST"])
def prompt_generator():
    values = {
        "idea": "",
        "platform": "midjourney",
        "style": "",
        "lighting": "",
        "ratio": "1:1",
        "keywords": "",
    }
    result = None
    if request.method == "POST":
        values = {
            "idea": request.form.get("idea", "").strip(),
            "platform": request.form.get("platform", "midjourney"),
            "style": request.form.get("style", ""),
            "lighting": request.form.get("lighting", ""),
            "ratio": request.form.get("ratio", "1:1"),
            "keywords": request.form.get("keywords", "").strip(),
        }
        result = build_prompt(**values)
    return render_template("prompt_generator.html", result=result, **values)


@generators_bp.route("/character", methods=["GET", "POST"])
def character():
    form = CharacterForm()
    prompt = process_character_form_data(request.form) if form.validate_on_submit() else None
    return render_template("character.html", form=form, prompt=prompt)
